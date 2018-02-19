# -*- coding: utf-8 -*-

#import import_laws
import xml.etree.ElementTree as etree
import os


class Norm:
    """A norm can be e.g. a paragraph. The juristic term norm may vary. The enbez is the number of the paragraph"""
    number_norms = 0
    number_norms_without_title = 0
    number_norms_without_enbez = 0


    def __init__(self, xml):
        self.xml = xml
        #print("init norm")
        self.builddate = self.xml.get("builddate")
        self.doknr = self.xml.get("doknr")
        try:
            self.titel = xml.find("metadaten").find("titel").text
        except AttributeError:
            self.titel = ""
            #print("Warnung: Keinen Titel")
            Norm.number_norms_without_title += 1
        try:
            self.enbez = xml.find("metadaten").find("enbez").text
        except AttributeError:
            self.enbez = ""
            #print("Warnung: keinen Enbez")
            Norm.number_norms_without_enbez += 1
        Norm.number_norms += 1


class Law:
    """A law consist of several norms"""
    number_laws = 0
    number_laws_without_footnotes = 0

    def __init__(self, path):
        tree = etree.parse(path)
        root = tree.getroot()
        self.references = []
        self.referenced_by = []
        self.norms = []
        self.jurabk = root[0].find("metadaten").find("jurabk").text
        self.langue = root[0].find("metadaten").find("langue").text
        abkuerzungsliste.append(self.jurabk)
        try:
            footnote_xml = root[0].find("textdaten").find("fussnoten").find("Content")
            footnote_extracted = etree.tostring(footnote_xml, encoding="utf-8", method="text")
            self.footnote = footnote_extracted.decode("utf-8")
            #print(self.footnote)

        except AttributeError:
            self.footnote = ""
            #print("Warnung: Keine mögliche Verknüpfung")
            Law.number_laws_without_footnotes += 1
        for child in root:
            self.norms.append(Norm(child))
        print("Init law: "+self.langue+" "+self.jurabk)
        Law.number_laws += 1

    def get_norm_names(self):
        """Return a list of the names from all norms in a law"""
        names = []
        for norm in self.norms:
            names.append(norm.titel)
            print(norm.titel)
        return names


def test_classes():
    """Create a class for every xml-file in the Source folder"""
    counter = 0
    for filename in os.listdir("Source"):
        if ".xml" in filename:
            all_laws.append(Law("Source/"+filename))
            print("Titel der Norm:" + all_laws[counter].langue)
            #if counter > 500:
            #    break
            counter += 1

    print(all_laws)


def test_norm_names():
    """Create a law form a concrete file and print the names of its norms"""
    a = Law("Source/BENR012420976.xml")
    print(a.get_norm_names())


def show_stats():
    print("Gesetze: " + str(Law.number_laws))
    print("Gesetze ohne Fussnote: " + str(Law.number_laws_without_footnotes))
    print("Normen: " + str(Norm.number_norms))
    print("Normen ohne Titel: " + str(Norm.number_norms_without_title))
    print("Normen ohne Enbez: " + str(Norm.number_norms_without_enbez))


def find_links():
    number_links = 0
    for law1 in all_laws:
        for law2 in all_laws :
            #print("We got a hit " + abk + " is referenced by " + law.langue)
            jurabk_to_match = law2.jurabk+" "
            if (jurabk_to_match in law1.footnote) and (law2 != law1):
                #print("We got a true hit " + law2.jurabk + " is referenced by " + law1.jurabk)
                #start debug area
                link_index = law1.footnote.find(law2.jurabk) #print the index where the link has been found
                print("Das Gesetz: "+law2.jurabk+" wurde an Stelle "+str(link_index)+" der Fußnote: "+law1.footnote+" gefunden.")
                #end debug area
                law1.references.append(law2)
                law2.referenced_by.append(law1)
                number_links += 1
    print("Es gibt " + str(number_links) + " Verknüpfungen zwischen den Gesetzen")


def find_most_referenced_law():
    references = 0
    for law in all_laws:
        if len(law.referenced_by) > references:
            most_referenced_law = law
            references = len(law.referenced_by)
    if references > 0:
        print("Das meist referenzierte Gesetz ist: " + most_referenced_law.langue)

def find_most_references_in_law():
    references = 0
    for law in all_laws:
        if len(law.references) > references:
            most_references_in_law = law
            references = len(law.references)
    if references > 0:
        print("Das Gesetz mit den meisten Referenzen ist: " + most_referenced_law.langue)


def get_len_reference_chain(law, parent_laws):
    print("Überprüfe subchain von: "+law.jurabk+" mit parents: "+print_jurabk_from_list(parent_laws))
    references = law.references
    if len(references) == 0:
        chain_length = 1  # when the law is a leaf in the tree
    else:
        chain_length = 1
        longest_sub_chain = 0
        for reference in references:
            if (not parent_laws) or (reference not in parent_laws):  # first condition is required to avoid error
                new_parent_laws = parent_laws
                new_parent_laws.append(law)
                sub_chain_len = get_len_reference_chain(reference, new_parent_laws)
                if sub_chain_len > longest_sub_chain:
                    longest_sub_chain = sub_chain_len
                    law_with_longest_subchain = reference
            else:
                print("found recursion")
        chain_length = chain_length+longest_sub_chain
    return chain_length


def get_longest_reference_chain():
    longest_law_chain = 0
    longest_chain_law = ""
    for law in all_laws:
        ref_len = get_len_reference_chain(law, [])
        print("---------------------------------------------------")
        if ref_len > longest_law_chain:
            longest_law_chain = ref_len
            longest_chain_law = law
    print("Längste Gesetzeskette ist " + longest_chain_law.jurabk + " mit " + str(longest_law_chain) + " Gesetzen.")


def print_jurabk_from_list(law_list):
        output = ""
        for law in law_list:
            output+=" > "+law.jurabk
        return output


chained_laws = []
all_laws = []
all_laws2 = {}
abkuerzungsliste = []
test_classes()
#test_norm_names()
show_stats()
print(abkuerzungsliste)
find_links()
find_most_referenced_law()
get_longest_reference_chain()
#print("ebin")
#empty = []
#print(get_len_reference_chain(all_laws[0], empty))
#print("ebun")
#print(get_len_reference_chain(all_laws[1]))
#print(get_len_reference_chain(all_laws[2]))
#TODO: maybe it's better to convert all_laws from a list to a dictionary #looked into it and dicts aren't really that fun
#TODO: update reference chain finder to memorize path (in order to return not only length but also the path itself)

