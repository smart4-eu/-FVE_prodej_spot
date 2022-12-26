# V�po�et pr�m�rn� spotov� ceny

Skript dok�e zpracovat data z distribu�n�ho port�lu �EZu a doplnit je o cenu za MWh v � a kurzem z �NB platn�m v dan� okam�ik p�etoku.

Data o cen� elektrick� energie se stahuj� z  https://www.ote-cr.cz
Kurz se stahuje z https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu

## Parametry skriptu

- -i/--input - n�zev vstupn�ho souboru csv pro zpracov�n�
- -o/--output - n�zev v�stupn�ho souboru csv
- -p/--progress - zobrazuje aktu�ln� zpracov�van� den

## Form�t vstupn�ho csv souboru

Skript zpracov�v� jen ��dky, kde je v prvn�m sloupe�ku datum ve form�tu a v druh�m sloupe�ku v�roba viz uk�zka:

```
"Datum";"-A/XXXX [kW]";"Status";
18.08.2022 00:15;0;nam��en� data OK;
18.08.2022 00:30;0;nam��en� data OK;
18.08.2022 00:45;0;nam��en� data OK;
18.08.2022 01:00;0;nam��en� data OK;
18.08.2022 01:15;0;nam��en� data OK;
18.08.2022 01:30;0;nam��en� data OK;
18.08.2022 01:45;0;nam��en� data OK;
18.08.2022 02:00;0;nam��en� data OK;
18.08.2022 02:15;0;nam��en� data OK;
18.08.2022 02:30;0;nam��en� data OK;
18.08.2022 02:45;0;nam��en� data OK;
18.08.2022 03:00;0;nam��en� data OK;
18.08.2022 03:15;0;nam��en� data OK;
18.08.2022 03:30;0;nam��en� data OK;
18.08.2022 03:45;0;nam��en� data OK;
18.08.2022 04:00;0;nam��en� data OK;
18.08.2022 04:15;0;nam��en� data OK;
18.08.2022 04:30;0;nam��en� data OK;
18.08.2022 04:45;0;nam��en� data OK;
```

## Vygenerov�n� vstupn�ch dat z https://pnd.cezdistribuce.cz/cezpnd2/external/dashboard/view ( https://dip.cezdistribuce.cz/ )

1. Vyberte obdob�, pro kter� chcete data zpracovat v polo�ce `Vlastn� obdob�`
2. Vyberte zobrazen� `Sloupcov� graf` a `02 Profil v�roby (-A)`

![cez](cez_distribuce.png)

3. Vagenerujte soubor pomoc� `Exportovat data` a `Zjednodu�en� CSV` 

![export](cez_export.png)