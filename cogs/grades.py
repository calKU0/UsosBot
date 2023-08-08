import sys
sys.path.append(".")
import discord
from discord import app_commands
from discord.ext import commands
import oauth2 as oauth
from database import operations
import json
from discord.ui import Select, View


class grades(commands.Cog):
    def __init__(self, bot:commands.Bot):
         self.bot = bot

    @app_commands.command(name="oceny", description="Twoje oceny")
    async def grades(self,interaction: discord.Interaction):
        ope = operations()
        if not ope.registered(interaction.user.id):
            await interaction.response.send_message("Nie jesteś zarejestrowany. Wpisz /register , aby się zarejestrować")
            return
        usosapi_base_url = ope.select(interaction.user.id, "endpoint")
        select = Select(placeholder="Wybierz semestr", options=[
        discord.SelectOption(label = "2022/2023 L", description = "Semestr letni 2022/2023", value="22/23L"),
        discord.SelectOption(label = "2022/2023 Z", description = "Semestr zimowy 2022/2023", value="22/23Z"),
        discord.SelectOption(label = "2021/2022 L", description = "Semestr letni 2021/2022", value="21/22L"),
        discord.SelectOption(label = "2021/2022 Z", description = "Semestr zimowy 2021/2022", value="21/22Z"),
        discord.SelectOption(label = "2020/2021 L", description = "Semestr letni 2020/2021", value="20/21L"),
        discord.SelectOption(label = "2020/2021 Z", description = "Semestr zimowy 2020/2021", value="20/21Z")
        ])
        view = View()
        view.add_item(select)
        await interaction.response.send_message(view=view)

        async def my_callback(interaction: discord.Interaction):
            access_token_key, access_token_secret = ope.select(interaction.user.id, "access_token")
            access_token = oauth.Token(access_token_key, access_token_secret)
            client = oauth.Client(ope.consumer(), access_token)

            resp, content = client.request(usosapi_base_url + f"services/grades/terms2?term_ids={select.values[0]}", "GET")
            if resp['status'] != '200':
                await interaction.response.send_message("Ups. Coś poszło nie tak. Spróbuj ponownie się zarejestrować")
            items = json.loads(content)
            dict = items.get('22/23L', {})

            embed = discord.Embed(title=f"Wykaz ocen semestru {select.values[0]} użytkownika {interaction.user.name}")
            embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
            i = 0

            for key, value in dict.items():
                if 'course_grades' in value:
                    course_grades = value['course_grades']
                    for course_grade in course_grades:
                        for grade_value in course_grade.values():
                            if grade_value is not None:
                                i+=1
                                value_symbol = grade_value.get('value_symbol')
                                passes = grade_value.get('passes')
                                resp, cont = client.request(usosapi_base_url + f"services/courses/course?course_id={key}&fields=name", "GET")
                                if resp["status"] != "200":
                                    interaction.response.send_message("Coś poszło nie tak")
                                course = json.loads(cont)
                                if float(value_symbol.replace(",",".")) >= 3:
                                    embed.add_field(name = str(i) + ". " + course["name"]["pl"], value = f"Grade: {value_symbol} :white_check_mark:", inline=False)
                                else:
                                    embed.add_field(name = str(i) + ". " + course["name"]["pl"], value = f"Grade: {value_symbol} :x:", inline=False)
            await interaction.response.send_message(embed=embed)
        select.callback = my_callback
         
async def setup(bot):
    await bot.add_cog(grades(bot))