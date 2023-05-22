import os

from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas

from config.settings.base import BASE_DIR, EMAIL_HOST_USER


class Ticket:
    def __init__(self, username, multiple_buys, user_email, user_name):
        self.username = username
        self.multiple_buys = multiple_buys
        self.service_name = "Yonesto"
        self.image_path = os.path.join(BASE_DIR, "static", "img", "unicapp.png")
        self.border_width = 5
        self.line_height = 20
        self.moneda = ""
        self.store_address = "Sala 2"
        self.user_email = user_email
        self.user_name = user_name

    def calculate_pagesize(self, purchases):
        width = 450
        lines = len(purchases)
        height = self.line_height * lines
        height += 260
        return (width, height)

    def draw_header(self, c, y, width):
        margin = 20 + self.border_width
        image_width = 100
        image_height = 100
        x = margin
        c.drawInlineImage(self.image_path, x, y, width=image_width, height=image_height)
        logo_height = image_height + margin
        service_name_y = (
            y + logo_height / 2 - self.line_height
        )  # Ubicar el service_name en la posición deseada
        c.setFont("Helvetica-Bold", 30)
        c.drawCentredString(width / 2, service_name_y, self.service_name)
        y = service_name_y - 20
        return y

    def draw_header_data_ticket(self, c, y, margin, width, buy_id, buy_date_purchase):
        c.setFont(
            "Helvetica", 8
        )  # Ajustar el tamaño de fuente para la información adicional
        c.drawCentredString(
            width / 2, y, f"Dirección de la tienda: {self.store_address}"
        )
        y -= self.line_height - 5

        c.drawCentredString(width / 2, y, f"Compra ID: {buy_id}")
        y -= self.line_height - 5

        c.drawCentredString(width / 2, y, f"Fecha y Hora: {buy_date_purchase}")
        y -= self.line_height + 15
        return y

    def draw_body_buys_products(self, c, y, margin, buy_products):
        c.setFont("Helvetica", 11)
        for item in buy_products:
            c.drawString(
                margin,
                y,
                f'{item["product_name"]}: {item["quantity"]} x ${item["price_product_sale_price"]:.2f} = ${item["amount"]:.2f}',
            )
            y -= self.line_height
        return y

    def draw_body_totals(
        self, c, y, margin, width, subtotal, buy_remaining_amount, payment
    ):
        c.setDash(1, 2)
        c.line(margin, y, width - margin, y)
        c.setDash(1, 0)
        y -= self.line_height

        c.setFont("Helvetica-Bold", 13)

        tax = 0
        total = subtotal + tax

        c.drawString(margin, y, f"Impuesto: ${tax:.2f}")
        y -= self.line_height

        c.drawString(margin, y, f"Total: ${total:.2f}")
        y -= self.line_height

        c.drawString(margin, y, f"Pagado: ${payment:.2f}")
        y -= self.line_height

        c.drawString(margin, y, f"Pago restante: ${buy_remaining_amount:.2f}")
        y -= 2 * self.line_height

        c.setFont("Helvetica", 12)
        c.drawString(margin, y, f"¡Gracias por su compra en {self.service_name}!")
        y -= self.line_height
        return y

    def generate_ticket(self, c, buy):
        buy_date_purchase = buy["date_purchase"]
        buy_id = buy["id"]
        buy_products = buy["buy_products"]
        buy_amount = buy["amount"]
        buy_remaining_amount = buy["remaining_amount"]
        buy_payment = buy_amount - buy_remaining_amount

        pagesize = self.calculate_pagesize(buy_products)
        width, height = pagesize
        c.setPageSize(pagesize)

        margin_white = 4
        margin = 10 + self.border_width + margin_white
        y = height - margin - 100  # Initial y after image
        y = self.draw_header(
            c=c,
            y=y,
            width=width,
        )

        y = self.draw_header_data_ticket(
            c=c,
            y=y,
            margin=margin,
            width=width,
            buy_id=buy_id,
            buy_date_purchase=buy_date_purchase,
        )
        y = self.draw_body_buys_products(
            c=c, y=y, margin=margin, buy_products=buy_products
        )
        y = self.draw_body_totals(
            c=c,
            y=y,
            margin=margin,
            width=width,
            subtotal=buy_amount,
            buy_remaining_amount=buy_remaining_amount,
            payment=buy_payment,
        )

        c.setLineWidth(self.border_width)
        c.rect(
            self.border_width / 2 + margin_white,
            self.border_width / 2 + margin_white,
            width - self.border_width - margin_white * 2,
            height - self.border_width - margin_white * 2,
        )
        c.showPage()

    def generate_tickets_and_send_mail(self, filename):
        c = canvas.Canvas(filename)
        for buy in self.multiple_buys:
            self.generate_ticket(c, buy)
        c.save()

        sender_email = EMAIL_HOST_USER
        destination_emails = [
            self.user_email,
        ]
        email = EmailMessage(
            f"Historial de pago en Yonesto - Gracias,{self.user_name}!",
            f"Hola: {self.user_name} a continuacion te adjuntamos todo tu historial de pago en Yonesto",
            sender_email,
            destination_emails,
        )
        filename_full = os.path.join(BASE_DIR, filename)
        with open(filename_full, "rb") as f:
            email.attach(filename, f.read(), "application/pdf")
        email.send()

        os.remove(filename_full)
