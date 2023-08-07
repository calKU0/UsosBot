import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
import oauth2 as oauth
from urllib.parse import parse_qs
import sys
sys.path.append(".")
import keys
from database import operations
from datetime import datetime
import json

class register(commands.Cog):
    def __init__(self, bot:commands.Bot):
         self.bot = bot

    @app_commands.command(name="register", description="Zarejestruj się do Usos'a")
    async def register(self,interaction: discord.Interaction):
        cities = set()
        with open("data/installations.json", encoding='utf-8') as file:
            data = json.load(file)
            for entry in data:
                cities.add(entry["city"])

        city_options = [discord.SelectOption(label=city, value=city) for city in cities]
        city_select = discord.ui.Select(placeholder="Wybierz miasto w którym studiujesz", options=city_options)
        view = View()
        view.add_item(city_select)
        await interaction.user.send(view=view)

        async def city_callback(interaction: discord.Interaction):
            selected_city = city_select.values[0]
            college_options = [discord.SelectOption(label=entry["collage_name"], value=entry["endpoint"]) for entry in data if entry["city"] == selected_city]
            college_select = discord.ui.Select(placeholder="Wybierz uczelnię", options=college_options)
            viewcollage = View()
            viewcollage.add_item(college_select)
            await interaction.response.send_message(view=viewcollage)

            async def college_callback(interaction: discord.Interaction):
                consumer = oauth.Consumer(keys.secrets("consumer_key"), keys.secrets("CONSUMER_SECRET"))
                usosapi_base_url = college_select.values[0]
                request_token_url = usosapi_base_url + 'services/oauth/request_token?scopes=studies|offline_access|grades&oauth_callback=oob'
                authorize_url = usosapi_base_url + 'services/oauth/authorize'
                access_token_url = usosapi_base_url + 'services/oauth/access_token'

                # Requesting a token
                client = oauth.Client(consumer)
                resp, content = client.request(request_token_url, "GET")
                if resp['status'] != '200':
                    raise Exception("Ups. Wystąpił problem. Czy napewno wybrałeś prawidłową uczelnię?")
                def _read_token(content):
                    content_str = content.decode()
                    arr = parse_qs(content_str)
                    arr = {key: value[0] for key, value in arr.items()}
                    return oauth.Token(arr['oauth_token'], arr['oauth_token_secret'])
                request_token = _read_token(content)

                # Hop on dms :)
                embed = discord.Embed(title="Rejestracja w USOS")
                embed.add_field(name="1. Aby korzystać z tego bota musisz przyznać mu prawa na usosie. Aby to zrobić wejdź w link:", value="%s?oauth_token=%s" % (authorize_url, request_token.key), inline=False)
                embed.add_field(name="2. Kliknij przyznaj dostęp", value="", inline=False)
                embed.add_field(name="3. Skopiuj PIN, który ci się wyświetli i wklej go w odpowiedzi poniżej", value="", inline=False)
                await interaction.response.send_message(embed=embed)
                try:
                    pin = await self.bot.wait_for("message", timeout=90)
                except Exception.TimeoutError():
                    interaction.user.send("Minał czas przeznaczony na rejestracje. Spróbuj ponownie")
                
                request_token.set_verifier(pin.content)
                client = oauth.Client(consumer, request_token)
                resp, content = client.request(access_token_url, "GET")
                try:
                    access_token = _read_token(content)
                    print(access_token)
                    ope = operations()
                    college_name = (entry["college_name"] for entry in data if entry["endpoint"] == college_select.values[0])
                    if not ope.registered(interaction.user.id):
                        ope.add_user(interaction.user.id, interaction.user.name, access_token, college_name, college_select.values[0], datetime.today())
                    else:
                        ope.modify_user(interaction.user.id, interaction.user.name, access_token, college_name, college_select.values[0], datetime.today())
                    await interaction.user.send("Zarejestrowano! Możesz teraz korzystać z pozostałych komend. Wpisz /help:all aby uzyskać listę dostępnych komend")
                except KeyError:
                    await interaction.user.send("Nie udało się uzyskać Access Token. Upewnij się że wpisałeś prawidłowy PIN")


            college_select.callback = college_callback
        city_select.callback = city_callback
        
        
async def setup(bot):
    await bot.add_cog(register(bot))

"""
        TODO:
        1. [DONE] Ogarnąć czy pin jest stały
            a) Jeśli tak to postawić baze na replicie albo w pracy --> DONE
            b) Jeśli nie to zobaczyć czy jest metoda autoryzacyjna co daje stały PIN --> Scope offline_access pozwala na to aby uzyskać stały token
        2. Postawić bota na replicie [ALMOST DONE]
        3. Poszukać manualnych testerów
        4. Nauczyć się pisać testy D:
        5. Dodawać stopniowo komendy zaczynajac od planu lekcji
""" 