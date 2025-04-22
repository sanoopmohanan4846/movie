from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from django. utils.timezone import now

from django.conf import settings
import stripe # type: ignore
from subscription.models import Subscription
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def subscription(request):
    subscription = {
        'basic':'price_1R5LgdChwEjeoK8BCTcCQi1z',
        'pro':'price_1R5LjxChwEjeoK8BDEnmYdg7',
    }
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
        
        price_id = request.POST.get('price_id')
        
        subscription = Subscription.objects.filter(user=request.user).first()
        if subscription:
            
            stripe_subscription = stripe.Subscription.retrieve(subscription.subscription_id)
            item = stripe_subscription['items']['data'][0]
            
            stripe.Subscription.modify(
                subscription.subscription_id,
                items = [{
                    'id':item['id'],
                    'price':price_id,
                }],
                cancel_at_period_end = False
            )
            
            price = stripe.Price.retrieve(price_id)
            product = stripe.Product.retrieve(price['product'])
            
            subscription.start_date = now()
            subscription.price = price['unit_amount']/100 
            subscription.product_name = product.name
            subscription.end_date = None
            subscription.canceled_at = None
            subscription.save()
            return redirect('my_sub')
            
        else:
            checkout_session = stripe.checkout.Session.create(
                line_items =[
                    {
                        'price':price_id,
                        'quantity':1,
                    },
                ],
                
                payment_method_types=['card'],
                mode='subscription',
                success_url = request.build_absolute_uri(reverse("create_subscription")) + f'?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=request.build_absolute_uri(f'{reverse("subscription")}'),
                customer_email=request.user.email,
                metadata={
                'user_id': request.user.id,
                }
                
            )
            
            return redirect(checkout_session.url, code=303)
        
    return render(request, 'subscription/subscription.html', { 'subscription':subscription })

def create_subscription(request):
    checkout_session_id = request.GET.get('session_id', None)
    
    # create subcription object in database
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    user_id = session.metadata.get("user_id")
    user = User.objects.get(id=user_id)
    subscription = stripe. Subscription.retrieve (session.subscription)
    price = subscription['items']['data'][0]['price']
    product_id = price ['product']
    product = stripe.Product.retrieve(product_id)
    
    if checkout_session_id:
        Subscription.objects.create(
            user=user,
            customer_id = session.customer,
            subscription_id = session.subscription,
            product_name = product.name,
            price = price ['unit_amount'] / 100,
            interval = price ['recurring'] ['interval'],
            start_date = datetime.fromtimestamp(subscription ['current_period_start']),
        )
    return redirect('my_sub')

def my_sub(request):
    if not request.user.is_authenticated:
            return redirect('login')
        
    subscription = Subscription.objects.filter(user=request.user).first()
    
    return render(request, 'subscription/my_sub.html', { 'subscription':subscription })


def cancel_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, user=request.user, subscription_id=subscription_id)
    
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end = True
    )
    
    subscription.canceled_at = now()
    stripe_subscription = stripe. Subscription.retrieve(subscription_id)
    subscription.end_date = datetime.fromtimestamp(stripe_subscription ['current_period_end'])
    subscription.save()
    return redirect('my_sub')


