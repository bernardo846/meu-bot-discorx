import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo="Sem motivo"):
    try:
        await membro.ban(reason=motivo)
        await ctx.send(f"🔨 {membro} foi banido.\nMotivo: {motivo}")
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para banir esse membro.")
    except Exception as erro:
        print(erro)
        await ctx.send("❌ Ocorreu um erro ao banir.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id_usuario: int):
    try:
        usuario = await bot.fetch_user(id_usuario)
        await ctx.guild.unban(usuario)
        await ctx.send(f"🔓 {usuario} foi desbanido.")
    except discord.NotFound:
        await ctx.send("❌ Esse usuário não está banido.")
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para desbanir.")
    except Exception as erro:
        print(erro)
        await ctx.send("❌ Ocorreu um erro ao desbanir.")


@bot.event
async def on_command_error(ctx, erro):
    if isinstance(erro, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão.")
    elif isinstance(erro, commands.MissingRequiredArgument):
        await ctx.send("❌ Faltou alguma informação no comando.")

import os

bot.run(os.getenv("TOKEN"))