# A feladat

Szomszédos Excel fájlok tartalmát összegyűjtő Excel makró, benne felugró üzenetekkel.

# Tanulságok

- spec.md alapján elsőre majdnem tökéletes lett, csak a makró másoláshoz megnyitotta a saját fájlját is, utána pedig bezára, amivel **a makró egyből kinyírta magát**... Ezt kiemelve a specifikációban és a promptban is egyből megjavította.
- Simán **le tudta fordítani** a makró minden üzenetét angolról magyarra.
- Érdemes az ilyen Excel tábla használatáról **egy rövid leírást berakni** magába az Excel fájba, pl. az első munkalapra.

# Konkrét promptok

Have a look at the @spec.md file. Can you create the VBA script for me as described there?

---

I have extended the @spec.md file with a new condition. The macro should not open the file again (for copying from) which it is running in.

---

Please modify the specification so that there is no assumption about the columns number and header to be copied. Whatever is in the 1st worksheet of the Excel file, that is the content to be collected from the other files into the current worksheet of the current file. The headers should be copied as well after clearing the current worksheet completely. If the headers in a file do not match the already copied ones, show an error message.

----

I have a new idea to make this even simpler to use: the Excel file containing the macro does not contain any data initially, just a single empty worksheet and the macro. If the macro is executed, that single worksheet should be the target where the other neighbour Excel files first worksheet should be merged. Please update the specification accordingly.

---

Please translate all messages of the macro to hungarian.
