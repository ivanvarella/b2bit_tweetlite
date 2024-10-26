import random
from django.core.management.base import BaseCommand
from users.models import CustomUser
from tweets.models import Tweet
from follows.models import Follow
from likes.models import Like


class Command(BaseCommand):
    help = "Popula a tabela CustomUser com dados de exemplo, cria tweets e estabelece relacionamentos de follow"

    def handle(self, *args, **kwargs):
        self.populate_users()
        self.create_tweets()
        self.create_follows()
        self.populate_likes()  # Chama a função para popular a tabela Likes

    def populate_users(self):
        users = [
            (
                "ada",
                "ada@django.com",
                "Ada",
                "Lovelace",
                "Pioneira da programação de computadores.",
            ),
            (
                "alan",
                "alan@django.com",
                "Alan",
                "Turing",
                "Matemático e cientista da computação.",
            ),
            (
                "grace",
                "grace@django.com",
                "Grace",
                "Hopper",
                "Cientista da computação e almirante da Marinha dos EUA.",
            ),
            (
                "linus",
                "linus@django.com",
                "Linus",
                "Torvalds",
                "Criador do núcleo Linux.",
            ),
            (
                "tim",
                "tim@django.com",
                "Tim",
                "Berners-Lee",
                "Inventor da World Wide Web.",
            ),
        ]

        for username, email, first_name, last_name, bio in users:
            user = CustomUser(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                bio=bio,
            )
            user.set_password("password123")  # Faz o hashing da senha
            user.save()
            # self.stdout.write(
            #     self.style.SUCCESS(f"Usuário {username} criado com sucesso.")
            # )

    def create_tweets(self):
        users = CustomUser.objects.all()  # Busca todos os usuários

        for user in users:
            for i in range(60):  # Cria 60 tweets por usuário
                content = f"This is tweet number {i + 1} from {user.username}!"  # Conteúdo do tweet
                tweet = Tweet(content=content, author=user)
                tweet.save()
                # self.stdout.write(
                #     self.style.SUCCESS(
                #         f"Tweet {i + 1} criado para o usuário {user.username}."
                #     )
                # )

    def create_follows(self):
        users = list(
            CustomUser.objects.all()
        )  # Busca todos os usuários e transforma em lista

        for user in users:
            # Filtra os usuários que não são o usuário atual
            available_users = []
            for u in users:
                if u != user:
                    available_users.append(u)

            # Escolhe entre 2 a 3 usuários aleatoriamente para seguir
            following_count = random.randint(2, 3)
            following_users = random.sample(available_users, following_count)

            for following_user in following_users:
                Follow.objects.get_or_create(follower=user, following=following_user)
                # self.stdout.write(
                #     self.style.SUCCESS(
                #         f"{user.username} agora está seguindo {following_user.username}."
                #     )
                # )

    def populate_likes(self):
        # Obtém todos os usuários e tweets
        users = CustomUser.objects.all()
        tweets = Tweet.objects.all()

        # Itera sobre cada usuário
        for user in users:
            # Armazena os IDs dos tweets que o usuário já curtiu
            liked_tweet_ids = set()

            # Continua até que o usuário tenha dado 40 likes
            while len(liked_tweet_ids) < 40:
                # Seleciona um tweet aleatório
                tweet = random.choice(tweets)

                # Verifica se o tweet já foi curtido por este usuário
                if (
                    tweet.id not in liked_tweet_ids
                    and not Like.objects.filter(user=user, tweet=tweet).exists()
                ):
                    # Cria o like
                    Like.objects.create(user=user, tweet=tweet)
                    liked_tweet_ids.add(
                        tweet.id
                    )  # Adiciona o ID do tweet aos já curtidos
                    # self.stdout.write(
                    #     self.style.SUCCESS(f"{user.username} curtiu o tweet {tweet.id}.")
                    # )
