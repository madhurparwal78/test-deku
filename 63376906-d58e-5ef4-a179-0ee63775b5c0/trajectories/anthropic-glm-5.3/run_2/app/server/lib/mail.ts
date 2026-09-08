import nodemailer from 'nodemailer';

let transport: any = null;

function smtp() {
  if (!transport) {
    transport = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: Number(process.env.SMTP_PORT ?? 1025),
      secure: false,
    });
  }
  return transport;
}

export async function sendMail(to: string, subject: string, text: string) {
  return smtp().sendMail({
    from: 'ravel@example.com',
    to,
    subject,
    text,
  });
}
