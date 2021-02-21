from redis_funcs import say
import random
import requests
import datetime
from time import sleep


# Trick to get the counting word
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

hosts = {
    "mountainlight": "http://192.168.178.29/api/",
    "joke": "https://official-joke-api.appspot.com/jokes",
    "weather": "http://api.openweathermap.org/data/2.5/weather?id=2759798&APPID=15e79497893ad73998faa51a71efe8c1&units=metric"
}


class Actions:
    @staticmethod
    def say(tree, text):
        say(text)

    @staticmethod
    def sayrandom(tree, options):
        say(random.choice(options))

    @staticmethod
    def saytime(tree, _):
        time = datetime.datetime.now()
        say(time.strftime("The time is %H %M"))

    @staticmethod
    def saytimenice(tree, _):
        time = datetime.datetime.now()

        hour = time.hour

        minute = time.minute

        # We're talking towards the next hour, so increase it by 1
        if minute > 32:
            hour += 1
        hour = hour % 12

        minute = (5 * round(minute/5)) % 60

        # We don't usually say 0 hours, we say 12
        if hour == 0:
            hour = 12

        # Handle the different cases
        if minute == 0:
            s = f"It is {hour} 'o clock"
        elif minute == 45:
            s = f"It is quarter to {hour}"
        elif minute == 15:
            s = f"It is quarter past {hour}"
        elif minute == 30:
            s = f"It is half past {hour}"
        elif minute > 30:
            s = f"It is {60 - minute} to {hour}"
        else:
            s = f"It is {minute} past {hour}"

        say(s)


    @staticmethod
    def saydate(tree, _):
        time = datetime.datetime.now()

        number = ordinal(time.day)
        s = time.strftime(f"It is %A the {number} of %B, at %H %M")
        say(s)

    # TODO: replace with external tool through REDIS
    @staticmethod
    def apicall(tree, parameters):
        host = hosts[parameters['host']]
        method = parameters['method']
        command = parameters['command']
        body = parameters.get('body')

        if method == 'put':
            requests.put(host + command, data=body)

    # TODO: replace with action through mirror code?
    @staticmethod
    def sayweather(tree, _):
        host = hosts['weather']
        r = requests.get(host)
        w = r.json()
        starter = random.choice([
            "It is currently",
            "It is now",
            "The weather right now is"
        ])
        t = round(w['main']['temp'])
        temp = random.choice([
            f"with a temperature of {t} degrees",
            f"at {t} degrees",
            f", {t} degrees celcius"
        ])

        s = f"{starter} {w['weather'][0]['main']} {temp}."
        say(s)

    @staticmethod
    def sayjoke(tree, _):
        j = requests.get(f"{hosts['joke']}/general/random")
        joke = j.json()[0]
        s = joke['setup'] + ' ' + joke['punchline']
        say(s)

    @staticmethod
    def nerdjoke(tree, _):
        j = requests.get(f"{hosts['joke']}/programming/random")
        joke = j.json()[0]
        s = joke['setup'] + ' ' + joke['punchline']
        say(s)

    @staticmethod
    def sleep(tree, interval):
        sleep(interval)