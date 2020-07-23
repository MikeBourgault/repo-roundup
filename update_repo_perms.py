import csv
import requests
import click
import configparser

@click.group()
def cli():
    pass   


@click.command()
@click.option("--team", help="Team to change.", required=True, type=str)
@click.option("--path", help="Path to CSV of repos.", required=True, type=str)
def update_repo_perms(team, path):
    
    repo_list = []
    config = configparser.ConfigParser()
    config.read('config.py')
    org_name = config['DEFAULT']['org_name']
    username = config['DEFAULT']['username']
    token = config['DEFAULT']['token']

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in row:
                repo_list.append(item)

    
    print("Which permission do you want to grant to %s for the following repos: \n %s" % (team, str(repo_list)))
    print("Options Include: pull, triage, push, maintain, admin")
    permission = input()

    fields = '{"permission": "%s"}' % (permission)

    for repo in repo_list:
        api_url = 'https://api.github.com/orgs/%s/teams/%s/repos/%s/%s' % (org_name, team, org_name, repo)
        response = requests.put(api_url, data=fields, auth=(username,token))
        if response.status_code is 204:
            print("%s permissions granted to %s for %s repository." % (permission, team, repo))
        elif response.status_code is 422:
            print("Unprocessable Entity. Repo not owned by organization.")
        elif response.status_code is 404:
            print("Authorization failed. Please check credentials.")
        elif response.status_code is 400:
            print("Bad Request. Please adjust request.")
        else:
            print("Unknown Error. %s" % response.status_code)
         

cli.add_command(update_repo_perms)

if __name__ == "__main__":
    cli()