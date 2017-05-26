from . import conekta

def create_customer(data):
    conekta.api_key = "key_xjYBs3oatsrrMmf1tEWf3A"
    conekta.api_version = "2.0.0"
    try:
      customer = conekta.Customer.create({
        'name': data.get("name"),
        'email': data.get("email"),
        'phone': data.get("phone"),
        'payment_sources': [{
          'type': 'card',
          'token_id': data.get("conekta_card")
        }]
      })
      return customer
    except conekta.ConektaError as e:
      print e.message
      return None

def create_card(user, data):
    conekta.api_key = "key_xjYBs3oatsrrMmf1tEWf3A"
    conekta.api_version = "2.0.0"
    try:
        customer = conekta.Customer.find(user.conekta_customer)
        card = customer.createPaymentSource({
            "type": "card",
            "token_id": data.get("conekta_card")
        })
        return card
    except conekta.ConektaError as e:
      print e.message
      return None

def delete_card(user, card):
    conekta.api_key = "key_xjYBs3oatsrrMmf1tEWf3A"
    conekta.api_version = "2.0.0"
    try:
        customer = conekta.Customer.find(user.conekta_customer)
        card_iteration_delete = 0
        for idx,payment_sources in enumerate(customer.payment_sources):
            if payment_sources.id == card.conekta_card:
                card_iteration_delete = idx
        customer.payment_sources[card_iteration_delete].delete()
        return True
    except conekta.ConektaError as e:
      print e.message
      return False

def set_default_card(user, card):
  conekta.api_key = "key_xjYBs3oatsrrMmf1tEWf3A"
  conekta.api_version = "2.0.0"
  try:
      customer = conekta.Customer.find(user.conekta_customer)
      customer.update({'default_payment_source_id': card.conekta_card})
      return True
  except conekta.ConektaError as e:
    print e.message
    return False

def create_order(user, subscription):
    conekta.api_key = "key_xjYBs3oatsrrMmf1tEWf3A"
    conekta.api_version = "2.0.0"
    try:
        customer = conekta.Customer.find(user.conekta_customer)
        order = conekta.Order.create({
            "currency": "MXN",
            "customer_info": {
                "customer_id": customer.id
            },
            "line_items": [{
                "name": "Pago: {0}".format(subscription.title),
                "unit_price": int(subscription.next_mount_pay)*100,
                "quantity": 1
            }],
            "charges":[{
                "payment_method": {
                    "type": "default"
                }
            }]
        })
        return order
    except conekta.ConektaError as e:
        print e.message
        return None
