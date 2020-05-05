# Documentation - PyNetGames

## I. Installation

Bon matteo tu le fais un comme un grand je sais pas comment on installe tout

## II. Lancement

Pour jouer à PyNetGames, vous devez tout d'abord lancer le serveur sur l'appareil de votre choix, pour cela faites:

```
python server.py
```
*Par défaut, le serveur utilise l'adresse ip de votre machine au port 5555*

Ensuite lancez le client en faisant:

```
python menu.py
```
*Par défaut, votre client considerera que le serveur se situe à votre adresse ip, au port 5555*

notez que si vous lancez le client sur un autre appareil que votre serveur, vous devez lui renseigner son adresse ip, 
pour cela rendez vous dans la rubrique **Configuration**

## III. Configuration

Vous avez la possibilité de choisir l'adresse ip de votre serveur, de choisir votre port et aussi de garder des valeurs par défaut pour les futurs lancements, pour se faire, faites:
```
python server.py -ip [ip/"auto"] -p [port] [-s pour sauvegarder par le futur]
```

Du coté client, pour configurer l'adresse ip, faites:

```
python config.py -ip [ip/"auto"] -p [port]
```
notez que par défaut, les valeurs sont respectivement l'adresse ip de votre machine, et 5555. Une fois la commande faite, vous n'avez plus à reconfigurer à part si votre serveur change d'adresse IP ou de port

Indiquer "auto" comme adresse ip renseignera l'adresse ip automatiquement si vous ne la connaissez pas
