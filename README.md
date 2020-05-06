# Documentation - PyNetGames

## I. Installation

Après avoir télechargé le dossier, il vous faudra d'abord rentrer dans l'environnement virtuel, ce qui permettra de n'avoir rien à installer sur votre ordinateur. Pour cela rendez vous avec votre invite de commandes dans le dossier principal et tapez :
```
source VirtualEnv/Scripts/activate
```

Vous pourrez en sortir à tout moment grâce a la commande :
```
deactivate
```

La dernière étape avant de pouvoir jouer est l'installation des librairies qui se fait via la commande :
```
pip install -r requirements.txt
```

## II. Lancement

Pour jouer à PyNetGames, vous devez tout d'abord lancer le serveur sur l'appareil de votre choix. Pour cela faites :

```
python server.py
```
*Par défaut, le serveur utilise l'adresse ip de votre machine au port 5555*

Ensuite lancez le client en tapant la commande :

```
python menu.py
```
*Par défaut, votre client considérera que le serveur se situe à votre adresse ip, au port 5555*

Notez que si vous lancez le client sur un autre appareil que votre serveur, vous devez lui renseigner son adresse ip.
Pour cela rendez vous dans la rubrique **Configuration**.

## III. Configuration

Vous avez la possibilité de choisir l'adresse ip de votre serveur, de choisir votre port et aussi de garder des valeurs par défaut pour les futurs lancements, pour se faire, effectuer :
```
python server.py -ip [ip/"auto"] -p [port] [-s pour sauvegarder les paramètres]
```

Du coté client, pour configurer l'adresse ip, vous pouvez utiliser :

```
python config.py -ip [ip/"auto"] -p [port]
```
Notez que par défaut, les valeurs sont respectivement l'adresse ip de votre machine, et 5555. Une fois la commande effectué, vous n'avez plus rien à configurer, à part si votre serveur change d'adresse IP ou de port.

Indiquer "auto" pour le paramètre ip permettra de la trouver automatiquement ( peut dysfonctionner si des VMs sont installés sur votre machine).
