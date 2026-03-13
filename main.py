import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    Race.objects.all().delete()
    Skill.objects.all().delete()
    Player.objects.all().delete()
    Guild.objects.all().delete()
    with open("players.json", "r") as players_file:
        players = json.load(players_file)
    for player_name, other in players.items():
        need_add_skill = other["race"]["skills"]
        for skill in need_add_skill:
            test = Race.objects.get_or_create(
                name=other["race"]["name"],
                description=other["race"]["description"])
            Skill.objects.get_or_create(
                name=skill["name"],
                bonus=skill["bonus"],
                race_id=test[0].id
            )
        Player.objects.create(
            nickname=player_name,
            email=other["email"],
            bio=other["bio"],
            race=Race.objects.get_or_create(
                name=other["race"]["name"],
                description=other["race"]["description"])[0],
            guild=Guild.objects.get_or_create(
                name=other["guild"]["name"],
                description=other["guild"]["description"]
            )[0] if other["guild"] is not None else None
        )


if __name__ == "__main__":
    main()
