from sita.users.models import User, Subscription
from sita.subscriptions.models import Subscription as Membership
from sita.payments.models import Payment
from datetime import datetime, timedelta
from sita.utils import conekta_sita
from sita.cards.models import Card

def generate_automatic_payment():
    subscriptions = Subscription.objects.filter(is_current=True)
    subscriptions = subscriptions.extra(
        where=["next_pay_date <= '{0}'".format(datetime.now())])
    for subscription in subscriptions:
        user = User.objects.get(id=subscription.user_id)
        if user.is_active:
            if user.automatic_payment:
                order = conekta_sita.create_order(user=user, user_subscription=subscription)
                if order["object"] == "order":
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
                        user_id = user.id,
                        subscription_id = subscription.id,
                    )
                    payment.save()
                    next_time_expirate = subscription.expiration_date + timedelta(minutes=subscription.next_time_in_minutes)
                    subscription_user = Subscription(
                        user_id=user.id,
                        time_in_minutes=subscription.next_time_in_minutes,
                        is_test=False,
                        is_current=True,
                        next_time_in_minutes=subscription.next_time_in_minutes,
                        next_mount_pay=subscription.next_mount_pay,
                        expiration_date=next_time_expirate,
                        next_pay_date=next_time_expirate,
                        title=subscription.title
                    )
                    subscription_user.save()
                    subscription.is_current = False;
                    subscription.save()
                if order["object"] == "error":
                    if order["type"] == "parameter_validation_error":
                        payment = Payment(
                            amount = subscription.next_mount_pay,
                            description = "La informacion de su tarjeta es incorrecta",
                            currency = "MXN",
                            title_subscription = subscription.title,
                            user_id = user.id,
                            subscription_id = subscription.id,
                            fail = True
                        )
                        payment.save()
                    if order["type"] == "processing_error":
                        reference_id_conekta = ''
                        for charge in order["data"]["charges"]["data"]:
                            reference_id_conekta = charge["id"]
                            card_last_four = charge["payment_method"]["last4"]
                            card_brand = charge["payment_method"]["brand"]
                        for line_items in order["data"]["line_items"]["data"]:
                            description = line_items["name"]
                        payment = Payment(
                            conekta_id = order["data"]["id"],
                            card_last_four = card_last_four,
                            card_brand = card_brand,
                            amount = subscription.next_mount_pay,
                            description = description,
                            reference_id_conekta = reference_id_conekta,
                            currency = "MXN",
                            title_subscription = subscription.title,
                            user_id = user.id,
                            subscription_id = subscription.id,
                            fail=True
                        )
                        payment.save()
                    fail_payments = Payment.objects.filter(
                        subscription_id=subscription.id,
                        fail=True).count()
                    if fail_payments == 1:
                        # send emai
                        next_pay_date = subscription.next_pay_date + timedelta(hours=72)
                        subscription.next_pay_date = next_pay_date
                        subscription.save()
                    if fail_payments == 2:
                        # send email
                        # cancel subscription
                        subscription.is_current = False;
                        subscription.save()
                        user.has_subscription = False
                        user.save()
            else:
                subscription.is_current = False;
                subscription.save()
                user.has_subscription = False
                user.save()
                # send email

def generate_payment(user, subscription_id):
    if Card.objects.user_has_card(user):
        user = User.objects.get(id=subscription.user_id)
        subscription = Membership.objects.get(id=subscription_id)
        if user.is_active:
            order = conekta_sita.create_order(user=user, subscription=subscription)
            if order["object"] == "order":
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
                    amount = subscription.amount,
                    description = description,
                    reference_id_conekta = reference_id_conekta,
                    currency = "MXN",
                    title_subscription = subscription.title,
                    user_id = user.id
                )
                payment.save()
                next_time_expirate = datetime.now() + timedelta(minutes=subscription.time_in_minutes)
                subscription_user = Subscription(
                    user_id=user.id,
                    time_in_minutes=subscription.time_in_minutes,
                    is_test=False,
                    is_current=True,
                    next_time_in_minutes=subscription.time_in_minutes,
                    next_mount_pay=subscription.amount,
                    expiration_date=next_time_expirate,
                    next_pay_date=next_time_expirate,
                    title=subscription.title
                )
                subscription_user.save()
            if order["object"] == "error":
                if order["type"] == "parameter_validation_error":
                    payment = Payment(
                        amount = subscription.next_mount_pay,
                        description = "La informacion de su tarjeta es incorrecta",
                        currency = "MXN",
                        title_subscription = subscription.title,
                        user_id = user.id,
                        subscription_id = subscription.id,
                        fail = True
                    )
                    payment.save()
                if order["type"] == "processing_error":
                    reference_id_conekta = ''
                    for charge in order["data"]["charges"]["data"]:
                        reference_id_conekta = charge["id"]
                        card_last_four = charge["payment_method"]["last4"]
                        card_brand = charge["payment_method"]["brand"]
                    for line_items in order["data"]["line_items"]["data"]:
                        description = line_items["name"]
                    payment = Payment(
                        conekta_id = order["data"]["id"],
                        card_last_four = card_last_four,
                        card_brand = card_brand,
                        amount = subscription.next_mount_pay,
                        description = description,
                        reference_id_conekta = reference_id_conekta,
                        currency = "MXN",
                        title_subscription = subscription.title,
                        user_id = user.id,
                        subscription_id = subscription.id,
                        fail=True
                    )
                    payment.save()
        else:
            return {"message":"This User is not active"}
    else:
        return {"message":"User dont have any card"}
