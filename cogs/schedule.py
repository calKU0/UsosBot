import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
import oauth2 as oauth
import sys
sys.path.append(".")
from database import operations
from datetime import datetime, timedelta
import json


class schedule(commands.Cog):
    def __init__(self, bot:commands.Bot):
         self.bot = bot
         self.usosapi_base_url = 'https://appsusos.uek.krakow.pl/'
         
    @app_commands.command(name="schedule", description="Get your today's schedule")
    async def schedule(self,interaction: discord.Interaction):  
        ope = operations()
        if not ope.registered(interaction.user.id):
            await interaction.user.send("Nie jesteś zarejestrowany. Wpisz /register , aby się zarejestrować")
            
        select = Select(placeholder="Wybierz zakres planu", options=[
            discord.SelectOption(label = "Dziś", description = "Dzisiejsze zajęcia"),
            discord.SelectOption(label = "Jutro", description = "Jutrzejsze zajęcia"),
            discord.SelectOption(label = "Tydzień", description = "Tygodniowy plan lekcji")
        ])
        view = View()
        view.add_item(select)
        await interaction.response.send_message(view=view)
        
        async def my_callback(interaction: discord.Interaction):
            access_token_key, access_token_secret = ope.select(interaction.user.id, "access_token")
            access_token = oauth.Token(access_token_key, access_token_secret)
            client = oauth.Client(ope.consumer(), access_token)
            today = datetime.now().date()
            if select.values[0] == "Dziś":
                start = today
                days = "1"
            if select.values[0] == "Jutro":
                start = str(today + timedelta(days=1))
                days = "1"
            if select.values[0] == "Tydzień":
                start = today - timedelta(days=today.weekday())
                days = "7"
            resp, content = client.request(self.usosapi_base_url + f"services/tt/student?start={start}&days={days}", "GET")
            if resp['status'] != '200':
                await interaction.response.send_message("Ups. Coś poszło nie tak. Spróbuj ponownie się zarejestrować")
            items = json.loads(content)
            print(items)
            #Potrzebuje kogoś kto ma plan na usosie, bo z jakiegoś powodu ja nie mam i mi wyrzuca pusty array, a chce to sformatować jakoś fajnie
                    
        select.callback = my_callback
        
async def setup(bot):
    await bot.add_cog(schedule(bot))