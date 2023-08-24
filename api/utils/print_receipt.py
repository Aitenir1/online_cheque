import pdfkit
from sh import lp
from escpos.printer import Network

from django.template.loader import render_to_string

from api.models import Order, OrderItem

from django.conf import settings

def print_receipt(customer=False, **kwargs) -> None:

    printer_ip = settings.PRINTER_IP

    if customer:
        order = kwargs['order']

        order_items = order.items.all()
        table = order.table
        comment = order.comments
    else:
        order_items = kwargs['items']
        print(order_items)
        table = kwargs['table']
        comment = kwargs['comment']

    printer = Network(printer_ip)
    printer.charcode('CP866')

    printer.set(align="center")
    if customer:
        printer.text("Web-Motion LLC\n")
        printer.text("Turusbekova 109/3, Bishkek\n")
        printer.text("www.motion-webllc.com\n\n")

        printer.text(f"Стол: {table}\n\n")

    printer.set(align="left")
    total_price = 0
    for order_item in order_items:
        print(order_item)
        if customer:
            name = order_item.dish.name_ru
            price = order_item.dish.price
            quantity = order_item.quantity
        else:
            name = order_item['dish'].name_ru
            price = order_item['dish'].price
            quantity = order_item['quantity']

        total_price += int(price) * int(quantity)
        printer.text(f"{name}{' '*(35-len(name))}{quantity}x{int(price)}={int(quantity*price)}c.\n")

    printer.text('\n\n')
    if customer:
        printer.text(f'Общий счет: {total_price}')
    else:
        if comment != '-':
            printer.text(f"{comment}\n")

    print("PRINTING")
    printer.cut()


        # printer.text(f"{order_item['dish'].name_en}\n")
    # printer.cut()
    # printer.ex


# def print_receipt(customer=False, **kwargs) -> None:
#     """
#     Function that queues the order receipt to the printer
#
#     :param order: The Order intance on which receipt is created
#     :param customer: Receipt for kithcet if True, for customer if False
#     """
#     # generate_html(order, customer)
#
#     if customer:
#         rendered_html = render_to_string('receipt_to_customer_template.html',
#                                          context={
#                                              'order': kwargs['order']
#                                              # 'order_items': kwargs['items'],
#                                              # 'table': kwargs['table'],
#                                              # 'time_created': kwargs['time_created'],
#                                              # 'total_price': kwargs['total_price']
#                                          })
#     else:
#         rendered_html = render_to_string('receipt_to_kitchen_template.html',
#                                          context={
#                                              'order_items': kwargs['items'],
#                                              'table': kwargs['table'],
#                                              'comment': kwargs['comment']
#                                              # 'time_created': kwargs['time_created']
#                                          })
#
#     with open('media/order_to_print.html', 'w+') as f:
#         f.write(rendered_html)
#
#     html2pdf('media/order_to_print.html', 'media/ready_to_print_order.pdf')
#
#     lp('media/ready_to_print_order.pdf')
#
#
# def html2pdf(input_file: str, output_file: str) -> None:
#     """
#     Function that converts HTML file to PDF receipt format
#
#     :param input_file: HTML file path (media/...)
#     :param output_file: The path where new PDF receipt is saved
#     """
#
#     try:
#         options = {
#             'page-size': 'A7',
#             # 'page-height': '1000mm',
#             # 'page-height': '200mm',
#             'margin-top': '0mm',
#             'margin-right': '0mm',
#             'margin-bottom': '0mm',
#             'margin-left': '0mm',
#             'encoding': 'UTF-8',
#             'no-outline': None,
#
#             "enable-local-file-access": ""
#         }
#
#         pdfkit.from_file(input_file, output_file, options=options)
#         print('Conversion successful. PDF created:', output_file)
#
#     except Exception as e:
#         print('Conversion failed:', e)
