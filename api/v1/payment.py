#!/usr/bin/python
# -*- coding: utf-8 -*-

def handle(socket, protocol, data):
    handler = mapper.handler.get(protocol)
    if handler is None:
        print 'handler not found'
        return
    fun = getattr(sys.modules[__name__], handler)
    fun(socket, data)

#微信支付
def wechat(socket, data):
    """ 微信支付
      - socket
      - data
    """
    pack_data = payment_pb2.Wechat_Pay_Response()
    unpack_data = payment_pb2.Wechat_Pay_Request()
    unpack_data.ParseFromString(data)

    order_id = unpack_data.order_id

    filter = {"_id": ObjectId(order_id)}
    order = Order.find_one(filter)
    
    if order is None:
        pack_data.error_code = payment_pb2.ERROR_ORDER_NOT_FOUND
        common.send(socket, payment_pb2.WECHAT_PAY, pack_data)
        return
    wechat = Wechat(base.WECHAT_PAY_APPKEY, base.WECHAT_PAY_APPID, base.WECHAT_PAY_MCHID)
    result = wechat.unified_order(out_trade_no, body, total_fee, notify_url)

    if "prepay_id" not in result:
        pack_data.error_code = payment_pb2.ERROR_PREPAY_FAILURE
        common.send(socket, payment_pb2.WECHAT_PAY, pack_data)
        return
    wechat_base = wechat.Base()
    wechat_base.from_dict(result)

def alipay(socket, data):
    """ 支付宝支付
      - socket 
      - data
    """
    pack_data = payment_pb2.Alipay_Pay_Response()
    unpack_data = payment_pb2.Alipay_Pay_Request()
    unpack_data.ParseFromString(data)

    order_id = unpack_data.order_id
    filter = {"_id": ObjectId(order_id)}
    order = Order.find_one(filter)

    if order is None:
        pack_data.error_code = payment_pb2.ERROR_ORDER_NOT_FOUND
        common.send(socket, payment_pb2.ALIPAY_PAY, pack_data)
        return
    alipay_config = {
        'private_key_path': base.ALIPAY_CONFIG['private_key_path']        
    }
    paramters = {
        "partner": base.ALIPAY_CONFIG['partner'],
        "seller_id": base.ALIPAY_CONFIG['seller_id'],
        "out_trade_no": order_id,
        "subject": 'iwasher',
        "body": "iwasher_body",
        "total_fee": 0.01,
        "notify_url": base.ALIPAY_CONFIG['notify_url'],
        "service": base.ALIPAY_CONFIG['service'],
        "payment_type": base.ALIPAY_CONFIG['payment_type'],
        "_input_charset": base.ALIPAY_CONFIG['input_charset'],
        "it_b_pay": base.ALIPAY_CONFIG['it_b_pay'],
        "sign_type": base.ALIPAY_CONFIG['sign_type']
    }
    
    result = Alipay(alipay_config).build_request_param(paramters)

    pack_data.paramters.body = result.get('body')
    pack_data.paramters.seller_id = result.get('seller_id')
    pack_data.paramters.total_fee = result.get('total_fee')
    pack_data.paramters.service = result.get('service')
    pack_data.paramters.input_charset = result.get('_input_charset')
    pack_data.paramters.it_b_pay = result.get('it_b_pay')
    pack_data.paramters.out_trade_no = result.get('out_trade_no')
    pack_data.paramters.payment_type = result.get('payment_type')
    pack_data.paramters.notify_url = result.get('notify_url')
    pack_data.paramters.sign_type = result.get('sign_type')
    pack_data.paramters.partner = result.get('partner')
    pack_data.paramters.sign = result.get('sign')
    pack_data.paramters.subject = result.get('subject')
    
    pack_data.error_code = payment_pb2.SUCCESS
    
    common.send(socket, payment_pb2.ALIPAY, pack_data)

