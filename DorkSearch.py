import requests
from sys import argv
from time import sleep
from os import system as exec
from colorama import Fore as Color
from random import random, randrange
from bs4 import BeautifulSoup as bsoup
from subprocess import check_output as execOutput


class Dork:
    def EngineGoogleSearch(Page, Query):
        Results = []
        base_url = 'https://www.google.com/search'
        Headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
        Params = {'q': Query, 'start': Page * 10}
        SleepTime = randrange(1, 3)+(random()*2)
        sleep(SleepTime)
        print(f'{Color.BLUE}[{Color.YELLOW}~{Color.BLUE}]{Color.WHITE} Sleeping {SleepTime}... (Simulating a human request)')
        def hisDork(tag):
            return tag.name == 'a' and tag.has_attr('href')
        GoogleResults = bsoup(requests.get(base_url, params=Params, headers=Headers).text, 'html.parser').find_all(hisDork)
        for AElm in GoogleResults:
            try:
                Link = AElm['href']
                if not Link.startswith('http') or Link.__contains__('google'):
                    continue
                Results.append(Link)
            except Exception as ignored:
                pass
        print(f'{Color.BLUE}[{Color.GREEN}✔{Color.BLUE}]{Color.WHITE} Results from Google (Page {Page}): {Color.RED}{Results}')
        return Results

    def ResultsToString(Results):
        try:
            NewResults = ''
            Index = 0
            for Result in Results:
                NewResults += Result
                NewResults += '\n'
                Index += 1
            return NewResults
        except Exception as ignored:
            return str(Results)

    def Search(Query, MaxPages=1):
        Output = 'Dork'
        ActualResponse = []
        Links = []
        Page = 0
        print(f'{Color.BLUE}[{Color.RED} START {Color.BLUE}]{Color.WHITE} DORK => {Color.YELLOW}\'{Color.RED}{Query}{Color.YELLOW}\'{Color.WHITE} PAGES => {Color.RED}{MaxPages}\n\n')
        sleep(0.2)
        print(f'{Color.BLUE}[{Color.YELLOW}~{Color.BLUE}]{Color.WHITE} Starting search... ')
        while True:
            if ActualResponse == [] and Page != 0:
                break
            ActualResponse = Dork.EngineGoogleSearch(Page, Query)
            for Link in ActualResponse:
                Links.append(Link)
            Page += 1
        print(f'{Color.BLUE}[{Color.YELLOW}~{Color.BLUE}]{Color.WHITE} Searching with ATSCAN...')
        exec(f'perl ATSCAN/atscan.pl --brandom -d {Query} -m all --level {int(MaxPages)} --time 1 --unique > {Output}.log')
        print(f'{Color.BLUE}[{Color.GREEN}✔{Color.BLUE}]{Color.WHITE} Search Finished.')
        for Line in execOutput(['cat', f'{Output}.log']).decode('utf-8').split('\n'):
            if not Line.__contains__('http'):
                continue
            if not Line.lower().__contains__('target'):
                continue
            LineDecoded = Line.split(' ')
            Link = LineDecoded[len(LineDecoded)-1]
            if Link in Links:
                continue
            try:
                Link = Link.replace('"', '')
                Link = Link.replace(',', '')
                Link = Link.replace('}', '')
                Link = Link.replace('{', '')
            except Exception as ignored:
                pass
            Links.append(Link)
        print(f'{Color.BLUE}[{Color.GREEN}✔{Color.BLUE}]{Color.WHITE} Results from ATSCAN: {Color.RED}{Dork.ResultsToString(Links)}')
        exec(f'rm {Output}.log')
        return Dork.ResultsToString(Links)

def Banner():
    exec('clear')
    print(f"""\033[1m                                                              
  {Color.GREEN}██████╗ ██╗   ██╗{Color.RED}██████╗  ██████╗ ██████╗ ██╗  ██╗██╗███╗   ██╗ ██████╗ 
  {Color.GREEN}██╔══██╗╚██╗ ██╔╝{Color.RED}██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██║████╗  ██║██╔════╝ 
  {Color.GREEN}██████╔╝ ╚████╔╝ {Color.RED}██║  ██║██║   ██║██████╔╝█████╔╝ ██║██╔██╗ ██║██║  ███╗
  {Color.GREEN}██╔═══╝   ╚██╔╝  {Color.RED}██║  ██║██║   ██║██╔══██╗██╔═██╗ ██║██║╚██╗██║██║   ██║
  {Color.GREEN}██║        ██║   {Color.RED}██████╔╝╚██████╔╝██║  ██║██║  ██╗██║██║ ╚████║╚██████╔╝
  {Color.GREEN}╚═╝        ╚═╝   {Color.RED}╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
    """)

def Help():
    print(f"""
    {Color.RED}
    Usage:
    
        {Color.GREEN}python {Color.WHITE}DorkSearch.py {Color.YELLOW}'[DORK]' [MAX-PAGES]
    
    {Color.WHITE}
    Example:
    
        {Color.GREEN}python {Color.WHITE}DorkSearch.py {Color.YELLOW}\'allintext:password "/" filetype:log\' {Color.WHITE}10
    """)

try:
    Banner()
    if argv[1] == '--help' or argv[1] == '-h':
        Help()
    else:
        # file deepcode ignore CommandInjection: <please specify a reason of ignoring this>
        results = Dork.Search(argv[1], argv[2])
        print(f'{Color.BLUE}[{Color.GREEN}✔{Color.BLUE}]{Color.WHITE} All results:\n\n{results}')
except Exception as e:
    Help()
    print(f'{Color.BLUE}[{Color.RED}✘{Color.BLUE}]{Color.RED} Error, check your arguments... {Color.GREEN}=> {Color.WHITE}{e}')
