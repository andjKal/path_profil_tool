# Path Profil Tool - QGIS Plugin [English version – Danish version below]

## Introduction
QGIS plugin developed by Kalundborg Municipality to more easily make line profile graphs anywhere in Denmark using dhm_terraen from https://www.dataforsyningen.dk.
Along with the profile graph the plugin calculates the linear distance, total elevation change, path distance (linear distance + total elevation change) as well as the total descent and accent of the path.

![Path Profile Tool profile graph](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/eda64ef9cc6a498db8363125695cd851/data "Path Profile Tool profile graph")

A token for dataforsyningens API is required to use the plugin. To get a token for using the plugin you can set up a free user on https://www.dataforsyningen.dk.

The plugin has been tested on QGIS versions 3.16 to 3.36.1 and work with these versions of QGIS. 

![Path Profil Tool](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/77af5d449514432ebcaa97d8bf606abe/data "Path Profil Tool plugin")

## How to install the plugin:

**1 -** Download the plugin as a .zip file by clicking on the "<> code" button and then "Download ZIP.

![Path Profil Tool](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/e5773864d7ba4ebebe7573e0d1f88105/data "Path Profil Tool QGIS plugin download")


**2 -** Open QGIS. Go to the plugins menu by clicking on "plugins" -> "Manage and Install Plugins..." from the top menu.

![QGIS plugin](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/ab4c9e762e214326b8e5978bc0cdd344/data "QGIS plugin")


**3 -** In the plugins menu choose **"Install from ZIP"** and locate the downloaded .zip file and install the plugin directly from the .zip file without unzipping.

![QGIS Install from zip](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1ec91e39f91c44c79de57d5a6899f2a4/data "QGIS Install from zip")


**4 -** The plugin is now ready to use.


## How to use the plugin:
**1 -** Start by loading in a line type layer you want to analyze into your QGIS project. This can be a layer with 1 or more features as long as you select the line feature you want to analyze in case of multiple features.
**2 -** Open the plugin by clicking on the icon ![Path Profil Tool icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1f2da0488d2c42e09fffb2e564b2aa42/data "Path Profil Tool QGIS plugin icon") or click on "Plugins" in the top menu and click on "Path Profile Tool" in the dropdown.

**NOTE - If you don't see neither the icon** ![Path Profil Tool icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1f2da0488d2c42e09fffb2e564b2aa42/data "Path Profil Tool QGIS plugin icon") **or "Path Profil Tool" in "Plugins" then open the plugins menu by clicking on "plugins" -> "Manage and Install Plugins..." from the top menu.**
**In the plugins menu click "Installed" and locate Path Profile Tool in the pluginlist and make sure to checkmark the plugin to make it active**

![QGIS installed apps](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/c048a6b2ff324782b98f06aeb4220a89/data "QGIS installed apps")


**3 -** Once the plugin is opened you can paste your token into lineedit. There is an option to save and automatically load the token for next time the plugin is opened if the “Save token” checkbox is checked. 
You can then select you line layer you want to analyze and choose if you want to use only the selected features by checking the checkbox “Use selected feature”.
Next you will have the option the select the interval in meters between the sampling points along you line feature. 
The lower the interval the more accurate it will be. However, this also drastically increases the processing time. It is therefore recommended to use lower intervals for shorter paths and higher intervals for longer paths.
Once all the settings have been set you can run the analysis by clicking the button “Run analysis” and you get a pop-up dialog box showing how far the processing is in percent.

![Path Profile Tool in progress](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/985878c4033449b6aaaad9342ca011f7/data "Path Profile Tool in progress")

**3 -** Once the processing is complete the plugin dialog automatically closes and a new dialog with line profile graph and statistics of the path. There is also an option to export the graph as an image. 

![Path Profile Tool profile graph](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/eda64ef9cc6a498db8363125695cd851/data "Path Profile Tool profile graph")

If you hover you mouse cursor over a point in the graph the corresponding point on the map will be highlighted to let you know exactly where the elevation and distance data were sampled from.

![Highlithing point on map](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/679152d9dfb84d3fab9844f6c64acdf1/data "Highlithing point on map")


# Path Profil Tool - QGIS Plugin [Dansk version]

## Introduktion
QGIS-plugin udviklet af Kalundborg Kommune til lettere at lave linjeprofildiagrammer hvor som helst i Danmark ved hjælp af dhm_terraen fra https://www.dataforsyningen.dk.
Sammen med profildiagrammet beregner plugin'et den lineære afstand, den samlede højdeforskel, stiafstanden (lineær afstand + samlet højdeforskel) samt den samlede nedstigning og opstigning af stien.

![Path Profile Tool profile graph](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/eda64ef9cc6a498db8363125695cd851/data "Path Profile Tool profile graph")

Et token til dataforsyningens API er nødvendig for at bruge plugin'et. For at få et token til at bruge plugin'et kan du oprette en gratis bruger på https://www.dataforsyningen.dk.

Plugin'et er blevet testet på QGIS-versionerne 3.16 til 3.36.1 og fungerer med disse versioner af QGIS. 

![Path Profil Tool](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/77af5d449514432ebcaa97d8bf606abe/data "Path Profil Tool plugin")

## Sådan installeres plugin'et:

**1 -** Download plugin'et som en .zip-fil ved at klikke på knappen "<> code" og derefter "Download ZIP".

![Path Profil Tool](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/e5773864d7ba4ebebe7573e0d1f88105/data "Path Profil Tool QGIS plugin download")


**2 -** Åbn QGIS. Gå til plugin-menuen ved at klikke på "Plugins" -> "Manage and Install Plugins..." fra topmenuen.

![QGIS plugin](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/ab4c9e762e214326b8e5978bc0cdd344/data "QGIS plugin")


**3 -** I plugin-menuen vælg **"Install from ZIP"** og find den downloadede .zip-fil og installer plugin'et direkte fra .zip-filen uden at pakke det ud.

![QGIS Install from zip](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1ec91e39f91c44c79de57d5a6899f2a4/data "QGIS Install from zip")


**4 -** Plugin'et er nu klar til brug.


## Sådan bruges plugin'et:
**1 -** Start med at indlæse et linjelag som du vil analysere i dit QGIS-projekt. Dette kan være et lag med en eller flere features, så længe du vælger den feature du vil analysere i tilfælde af flere features i laget.
**2 -** Åbn plugin'et ved at klikke på ikonet ![Path Profil Tool icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1f2da0488d2c42e09fffb2e564b2aa42/data "Path Profil Tool QGIS plugin icon") eller klik på "Plugins" i topmenuen og klik på "Path Profile Tool" i menuen.

**BEMÆRK - Hvis du ikke kan se hverken ikonet** ![Path Profil Tool icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1f2da0488d2c42e09fffb2e564b2aa42/data "Path Profil Tool QGIS plugin icon") **eller "Path Profil Tool" i "Plugins", så åbn plugin-menuen ved at klikke på "Plugins" -> "Manage and Install Plugins..." fra topmenuen.**
**I plugin-menuen klik på "Installed" og find Path Profile Tool i pluginlisten og sørg for at afkrydse plugin'et for at gøre det aktivt**

![QGIS installed apps](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/c048a6b2ff324782b98f06aeb4220a89/data "QGIS installed apps")


**3 -** Når plugin'et er åbnet kan du indsætte din token i lineedit. Der er en mulighed for at gemme og automatisk indlæse dit token næste gang plugin'et åbnes, hvis afkrydsningsfeltet "Save token" er markeret. 
Du kan derefter vælge det linjelag som du vil analysere og vælge om du kun vil bruge de valgte features ved at markere afkrydsningsfeltet "Use selected feature".
Derefter har du mulighed for at vælge intervallet i meter mellem prøvepunkterne langs din linje. 
Jo lavere intervallet er, desto mere præcist vil det være. Dette øger dog også drastisk behandlingstiden. Det anbefales derfor at bruge lavere intervaller for kortere stier og højere intervaller for længere stier.
Når alle indstillinger er sat, kan du køre analysen ved at klikke på knappen "Run analysis", og du får en pop-up-dialogboks som viser, hvor langt behandlingen er i procent.

![Path Profile Tool in progress](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/985878c4033449b6aaaad9342ca011f7/data "Path Profile Tool in progress")

**4 -** Når behandlingen er færdig lukkes plugin-dialogen automatisk og en ny dialog med linjeprofildiagram og statistik over stien vises. Der er mulighed for at eksportere diagrammet som et billede. 

![Path Profile Tool profile graph](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/eda64ef9cc6a498db8363125695cd851/data "Path Profile Tool profile graph")

Hvis du holder musemarkøren over et punkt i diagrammet vil det tilsvarende punkt på kortet blive fremhævet på kortet så du præcis ved, hvor højden og afstandsdataene blev beregnet.

![Highlithing point on map](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/679152d9dfb84d3fab9844f6c64acdf1/data "Highlithing point on map")
