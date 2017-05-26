from sita.users.models import User, Subscription
from sita.payments.models import Payment
from datetime import datetime, timedelta
from sita.utils import conekta_sita

def generate_payment():
    subscriptions = Subscription.objects.filter(is_current=True)
    subscriptions = subscriptions.extra(
        where=["next_pay_date <= '{0}'".format(datetime.now())])
    for subscription in subscriptions:
        user = User.objects.get(id=subscription.user_id)
        if user.is_active:
            next_time_expirate = subscription.expiration_date + timedelta(minutes=subscription.time_in_minutes)
            order = conekta_sita.create_order(user=user, subscription=subscription)
            if order.payment_status == "paid":
                reference_id_conekta = ''
                for charge in order.charges:
                    reference_id_conekta = charge.id
                    card_last_four = charge.payment_method.last4
                    card_brand = charge.payment_method.brand
                for line_items in order.line_items:
                    description = line_items.name

                payment = Payment(
                    conekta_id = order.id,
                    card_last_four = card_last_four,
                    card_brand = card_brand,
                    amount = subscription.next_mount_pay,
                    description = description,
                    reference_id_conekta = reference_id_conekta,
                    currency = "MXN",
                    title_subscription = subscription.title,
                    user_id = user.id
                )
                payment.save()
    print datetime.now()
    print "hey"
