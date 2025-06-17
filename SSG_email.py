import SSG_content # you need to import the file containing all of your content
import datetime
import smtplib
from email.message import EmailMessage

class DailyDigestEmail:

    def __init__(self):
        self.content = {'quote': {'include': True, 'content': SSG_content.get_random_quote()},
                        'weather': {'include': True, 'content': SSG_content.get_weather_forecast()},
                        'top_news':{'include': True, 'content': SSG_content.my_custom_function()},
                        'wikipedia': {'include': True, 'content': SSG_content.get_wikipedia_article()},}
        
        self.recipients_list = ['XXXX@gmail.com', 'XXXX@outlook.com']  # replace by email adresses

        self.sender_credentials = {'email': 'XXXX@gmail.com', # replace by your sender email address
                                   'password': ''} # replace by your sender password

    def send_email(self):
        # build email message, the email:example section of email module helps you
        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recipients_list)

        # add Plaintext and HTML content
        msg_body = self.format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['html'], subtype='html')

        # secure connection with STMP server using TLS encryption and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server: 
            server.starttls()
            server.login(self.sender_credentials['email'],
                         self.sender_credentials['password'])
            server.send_message(msg)

    """
    Generate email message body as Plaintext and HTML.
    """
    def format_message(self):
        ##############################
        ##### Generate Plaintext #####
        ##############################
        text = f'*~*~*~*~* Newsletter of the Day - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '*~*~* Quote of the Day *~*~*\n\n'
            text += f'"{self.content["quote"]["content"]["saying"]}" - {self.content["quote"]["content"]["meaning"]}\n\n'

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'*~*~* Current forecast for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]} *~*~*\n\n'
            text += f' {self.content['weather']['content']["time"].strftime('%d %b %H%M')}- {self.content['weather']['content']["temp"]}\u00B0C | {self.content['weather']['content']["weather"]}\n'
            text += '\n'

        # format top news
        if self.content['top_news']['include'] and self.content['top_news']['content']:
            text += '*~*~* Top News  *~*~*\n\n'
            for items in self.content['top_news']['content']['articles']: 
                text += f'{items["title"]}\n <{items['url']}> \n'
                text += '\n'


        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n{self.content["wikipedia"]["content"]["extract"]}'
     
 #########################
        ##### Generate HTML #####
        #########################
        html = f"""<html>
    <body>
    <center>
        <h1>Newsletter of the Day - {datetime.date.today().strftime('%d %b %Y')}</h1>
        """

        # format random quote DONE
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['saying']}"</i> - {self.content['quote']['content']['meaning']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2> 
        <table>
                    """

            
            html += f"""
            <tr>
                <td>
                    {self.content['weather']['content']['time'].strftime('%d %b %H%M')}
                </td>
                
                <td>
                    {self.content['weather']['content']['temp']}\u00B0C | {self.content['weather']['content']['weather']}
                </td>
            </tr>
                        """               

            html += """
            </table>
                    """

        # top news DONE
        if self.content['top_news']['include'] and self.content['top_news']['content']:
            html += """
        <h2>Top News</h2>
                    """

            for items in self.content['top_news']['content']['articles']: # top ten
                html += f"""
        <b><a href="{items['url']}">{items['title']}</a></b><p>
                        """

        # format Wikipedia article DONE
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
</html>
                """

        return {'text': text, 'html': html}

if __name__ == '__main__':
    email = DailyDigestEmail()

    ##### test format_message() #####
    print('\nTesting email body generation...')
    message = email.format_message()

    # print Plaintext and HTML messages
    print('\nPlaintext email body is...')
    print(message['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])

    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])

     ##### test send_email() #####
    print('\nSending test email...')
    email.send_email()