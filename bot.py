import discord
from discord.ext import commands

# 봇의 기본 설정
intents = discord.Intents.all()  # 모든 intents 활성화
bot = commands.Bot(command_prefix="!", intents=intents)

# 인증 완료된 사용자를 추적하기 위한 세트
authenticated_users = set()

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 온라인 상태입니다.')

@bot.event
async def on_member_join(member):
    # 새로운 유저에게 DM으로 인증 요청 메시지 전송
    try:
        await member.send("안녕하세요! 서버에 오신 것을 환영합니다! 인증을 완료하려면 이 DM에서 `!인증` 명령어를 입력해주세요.")
    except discord.Forbidden:
        # DM 전송 실패 시 콘솔에 경고 메시지 출력
        print(f"{member}에게 DM을 보낼 수 없습니다.")

@bot.command()
async def 인증(ctx):
    # 서버에 속한 멤버인지 확인
    if ctx.guild is not None:
        await ctx.send("이 명령어는 DM에서만 사용할 수 있습니다.")
        return
    
    # 이미 인증된 사용자 확인
    if ctx.author.id in authenticated_users:
        await ctx.send(f"{ctx.author.mention}님, 이미 인증을 완료한 상태입니다.")
        return

    # 인증 완료 처리
    authenticated_users.add(ctx.author.id)

    # 유저가 속한 모든 서버에서 역할 부여 시도
    for guild in bot.guilds:
        member = guild.get_member(ctx.author.id)
        if member:
            role = discord.utils.get(guild.roles, name="유저")  # 역할 이름 확인 필요
            if role:
                await member.add_roles(role)
                await ctx.send(f"{ctx.author.mention}님, 인증이 완료되었습니다! `{guild.name}` 서버에서 역할이 부여되었습니다.")
            else:
                await ctx.send(f"`{guild.name}` 서버에 '유저' 역할이 없습니다. 서버 관리자에게 문의해주세요.")

bot.run('MTIxMzY1MjE5MjgxMzI2MDgyMA.GHi-0V.0L5Ak7VJteusNT0q9FzBSVpXZ4K7qD1uuld6OQ')
