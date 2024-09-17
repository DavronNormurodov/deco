import threading

from rest_framework import serializers

from core.bot import send_alert
from product.models.order import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    selected_quantity = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        if quantity := attrs.pop('selected_quantity', 0):
            attrs['quantity'] = quantity
        return super(OrderItemSerializer, self).validate(attrs)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'selected_quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items = validated_data.pop('order_items', None)
        order = super(OrderSerializer, self).create(validated_data)

        send_data = f"#{order.id}\n\n" \
                    f"👤 Информация о заказчике\n\n" \
                    f"🙎‍♂ {validated_data.get('full_name')}\n" \
                    f"📱 +{validated_data.get('phone_number')}\n" \
                    f"✉ {validated_data.get('mail')}\n" \
                    f"📍 {validated_data.get('address')}\n\n\n" \
                    f"🛒 Информация о продукте\n\n"

        sum_all = 0

        for i, item in enumerate(order_items):
            try:
                price = item.get('product').price
            except:
                price = item.get('product').price if not item.get('product').is_sale else item.get('product').sale_price
            send_data += f"🛍 {i + 1}. {item.get('product').name} " + "💶 {:0,.2f}\n".format(price) + \
                         f"🧾 {item.get('quantity')} шт\n" + \
                         "💶 {:0,.2f}\n\n".format(item.get('quantity') * price)
            sum_all += item.get('quantity') * price

            OrderItem.objects.create(order_id=order.id, product=item.get('product'),
                                     quantity=item.get('quantity'))
        # send telegram
        send_data += "💶 Общая заказ сумма: {:0,.2f}".format(sum_all)
        threading.Thread(target=send_alert, args=[send_data]).start()
        return order
