class OWLEncoder:
    """
    OWL-code generator
    """

    def __init__(self, iri):
        self.__iri = iri

        self.__content = ""

        self.__classes = []
        self.__unions = {}
        self.__restrictions = {}
        self.__csc_relations = []
        self.__ci_relations = []
        self.__cp_relations = []
        self.__cpvd_relations = []
        self.__cpvi_relations = []

        self.__owl_init()

    def __owl_init(self):
        """
        Add owl header information
        :return: None
        """
        header = "<?xml version=\"1.0\"?>\n" + \
                 "<rdf:RDF xmlns=\"{0}#\"\n" + \
                 "     xml:base=\"{0}\"\n" + \
                 "     xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n" + \
                 "     xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n" + \
                 "     xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n" + \
                 "     xmlns:xml=\"http://www.w3.org/XML/1998/namespace\"\n" + \
                 "     xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\">\n" + \
                 "     <owl:Ontology rdf:about=\"{0}\"/>\n\n\n\n"

        self.__content = header.format(self.__iri)

    def set_iri(self, iri):
        """
        Change iri of the ontology
        :param iri: new iri
        :return: None
        """
        self.__content.replace(self.__iri, iri)
        self.__iri = iri

    def add_class(self, class_name):
        """
        Add new owl-class to the ontology
        :param class_name: new class name
        :return: None
        """

        self.__classes.append(class_name)

    def add_union(self, link_word, triples):
        """
        Add union to the ontology
        self_unions[link-word] => list of triples with these link-word
        :return:
        """

        self.__unions[link_word] = triples

    def get_union_by_link_word(self, link_word):
        """
        :return: self.__unions[link_word]
        """

        if link_word in self.__unions.keys():
            return self.__unions[link_word]
        else:
            return None

    def get_restriction_by_key(self, restriction_key):
        """
        :return: self.__restrictions[<Concept1 Name>_<Link-word>]
        """

        if restriction_key in self.__restrictions.keys():
            triples = []
            c1 = restriction_key.split('_')[0]
            link_word = restriction_key.split('_')[1]
            for c2 in self.__restrictions[restriction_key]:
                triples.append([c1, link_word, c2])
            return triples
        else:
            return None

    def add_restriction(self, restriction, related_concepts):
        """
        Add restrictions - the case when link-word connect concept c1 to several concepts
        self.__restrictions[<Concept1 Name>_<Link-word>] => list of related concepts
        :return:
        """

        self.__restrictions[restriction] = related_concepts

    def add_csc_relation(self, class_name, subclass_name):
        """
        Add new class-subclass relation to the ontology
        """
        self.__csc_relations.append([class_name, subclass_name])

    def add_ci_relation(self, concept_name, instance):
        """
        Add new concept-instance relation to the ontology
        """
        self.__ci_relations.append([concept_name, instance])

    def add_cp_relation(self, concept_name, property_name):
        """
        Add new concept-property relation to the ontology
        """
        self.__cp_relations.append([concept_name, property_name])

    def add_cpvd_relation(self, concept_name, property_name, property_value):
        """
        Add new concept-property-direct_value relation to the ontology
        """
        self.__cpvd_relations.append([concept_name, property_name, property_value])

    def add_cpvi_relation(self, concept_name, property_name, property_value):
        """
        Add new concept-property-indirect_value relation to the ontology
        """
        self.__cpvi_relations.append([concept_name, property_name, property_value])

    def __encode_all_unions(self):
        """
        Generate owl-code for unions
        :return: owl-code string
        """

        owl_code = ""

        for union in self.__unions:
            link_word = union
            domains = [triple[0] for triple in self.__unions[link_word]]
            ranges = [triple[2] for triple in self.__unions[link_word]]

            owl_comment = "     <!-- {0}#{1} -->\n"
            owl_unions = self.__encode_union(link_word, domains, ranges)

            owl_code += owl_comment.format(self.__iri, link_word) + owl_unions + '\n\n'

        return owl_code

    def __encode_all_restrictions(self):
        """
        Generate owl-code for restrictions
        :return: owl-code string
        """

        owl_code = ""

        for restriction in self.__restrictions:
            concept, link_word = (restriction.split('_'))

            owl_comment = "     <!-- {0}#{1} -->\n"
            owl_restrictions = self.__encode_restriction(concept, link_word, self.__restrictions[restriction])

            owl_code += owl_comment.format(self.__iri, link_word) + owl_restrictions + '\n\n'

        return owl_code

    def __encode_classes(self):
        """
        Generate owl-code for classes
        :return: owl string
        """

        owl_header = "     <!--" + \
                     "\n     ///////////////////////////////////////////////////////////////////////////////////////" + \
                     "\n     //" + \
                     "\n     // Classes" + \
                     "\n     //" + \
                     "\n     ///////////////////////////////////////////////////////////////////////////////////////" + \
                     "\n     -->\n"

        owl_code = owl_header

        for class_name in self.__classes:
            # All of spaces must be replaced with underscores
            class_name = class_name.replace(' ', '_')

            owl_comment = "\n\n\n\n     <!-- {0}#{1} -->\n"
            owl_pattern = "\n     <owl:Class rdf:about = \"{0}#{1}\"/>"

            owl_code += owl_comment.format(self.__iri, class_name) + owl_pattern.format(self.__iri, class_name)

        return owl_code

    def __encode_csc_relationship(self, class_name, subclass_name):
        """
        Add CSC relationship to the ontology. (Ex: Apple tree - subclass of trees)
        :param class_name: name of base class
        :param subclass_name: name of subclass
        :return: owl-code string
        """

        # All of spaces must be replaced with underscores
        class_name = class_name.replace(' ', '_')
        subclass_name = subclass_name.replace(' ', '_')

        owl_pattern = "\n     <owl:Class rdf:about = \"{0}#{1}\">\n" + \
                      "     \t<rdfs:subClassOf rdf:resource= \"{0}#{2}\"/>\n" + \
                      "     </owl:Class>\n"

        return owl_pattern.format(self.__iri, subclass_name, class_name)

    def __encode_ci_relationship(self, class_name, example):
        """
        Add CI relationship to the ontology. (Concept - Instance)
        Ex. BMW is an example of Car.
        :return: owl-code string
        """

        # All of spaces must be replaced with underscores
        class_name = class_name.replace(' ', '_')
        example = example.replace(' ', '_')

        owl_pattern = "     <owl:NamedIndividual rdf:about=\"{0}#{2}\">\n" + \
                      "     \t<rdf:type rdf:resource=\"{0}#{1}\"/>\n" + \
                      "     </owl:NamedIndividual>"

        return '\n' + owl_pattern.format(self.__iri, class_name, example) + '\n'

    def __encode_cp_relationship(self, class_name, class_property):
        """
        Add CP relationship to the ontology. (Concept - Property)
        Ex. Weather is Warm.
        :return: owl-code string
        """

        # All of spaces must be replaced with underscores
        class_name = class_name.replace(' ', '_')
        class_property = class_property.replace(' ', '_')

        owl_pattern = "\n     <owl:ObjectProperty rdf:about= \"{0}#{2}\">\n" + \
                      "     \t\t<rdf:type rdf:resource=\"http://www.w3.org/2002/07/owl#FunctionalProperty\" />\n" + \
                      "     \t\t<rdfs:domain rdf:resource= \"{0}#{1}\" />\n" + \
                      "     \t\t<rdfs:range rdf:resource= \"{0}#{2}\" />\n" + \
                      "     </owl:ObjectProperty>\n"

        return owl_pattern.format(self.__iri, class_name, class_property)

    def __encode_cpvd_relationship(self, class_name, class_property, value):
        """
        Add CPVD relationship to the ontology. (Concept - Property - Direct Value)
        Ex. Ball has shape Circle.
        :return: owl-code string
        """

        # All of spaces must be replaced with underscores
        class_name = class_name.replace(' ', '_')
        class_property = class_property.replace(' ', '_')
        value = value.replace(' ', '_')

        owl_pattern = "\n     <owl:ObjectProperty rdf:about= \"{0}#{1}\">\n" + \
                      "     \t\t<rdf:type rdf:resource=\"http://www.w3.org/2002/07/owl#FunctionalProperty\" />\n" + \
                      "     \t\t<rdfs:domain rdf:resource= \"{0}#{2}\" />\n" + \
                      "     \t\t<rdfs:range rdf:resource= \"{0}#{3}\" />\n" + \
                      "     </owl:ObjectProperty>\n"

        return owl_pattern.format(self.__iri, class_property, class_name, value)

    def __encode_cpvi_relationship(self, class_name, class_property, value):
        """
        Add CPVI relationship to the ontology. (Concept - Property - Indirect Value)
        Ex. Blood Veins contains Blood.
        :return: owl-code string
        """

        # All of spaces must be replaced with underscores
        class_name = class_name.replace(' ', '_')
        class_property = class_property.replace(' ', '_')
        value = value.replace(' ', '_')

        owl_pattern = "\n     <owl:ObjectProperty rdf:about= \"{0}#{1}\">\n" + \
                      "     \t\t<rdfs:domain rdf:resource= \"{0}#{2}\" />\n" + \
                      "     \t\t<rdfs:range rdf:resource= \"{0}#{3}\" />\n" + \
                      "     </owl:ObjectProperty>\n"

        return owl_pattern.format(self.__iri, class_property, class_name, value)

    @staticmethod
    def __encode_restriction(class_name, class_property, restriction):
        """
        Add restrictions to the ontology.
        :param class_name:
        :param class_property:
        :param restriction:
        :return: owl-code
        """

        class_name = class_name.replace(' ', '_')
        class_property = class_property.replace(' ', '_')

        owl_pattern = "     <owl:Class rdf:about = \"{0}\">\n" + \
                      "     <rdfs:subClassOf>\n" + \
                      "     <owl:Restriction>\n" + \
                      "     <owl:onProperty rdf:resource = \"#{1}\">\n"

        owl_pattern = owl_pattern.format(class_name, class_property)

        for item in restriction:
            item = item.replace(' ', '_')
            owl_pattern += "     \t<owl:someValueFrom rdf:resource = \"#{}\"/>\n".format(item)

        owl_pattern += "     \t</owl:onProperty>\n" + \
                       "     \t</owl:Restriction>\n" + \
                       "     \t</rdfs:subClassOf>\n" + \
                       "     </owl:Class>\n"

        return "\n" + owl_pattern + "\n"

    @staticmethod
    def __encode_union(link_word, rdfs_domain, rdfs_range):
        """
        Add unions to the ontology.
        :param link_word:
        :param rdfs_domain:
        :param rdfs_range:
        :return: owl-code
        """

        owl_pattern = "     <owl:ObjectProperty rdf:about = \"{0}\">\n" + \
                      "     \t<rdfs:domain>\n" + \
                      "     \t\t<owl:Class>\n" + \
                      "     \t\t\t<owl:unionOf rdf:parseType=\"Collection\">"

        owl_pattern = owl_pattern.format(link_word)

        domain_pattern = ""

        for item in rdfs_domain:
            item = item.replace(' ', '_')
            domain_pattern += "     \t\t\t\t<owl:Class rdf:about=\"#{0}\" />\n".format(item)

        owl_pattern += '\n' + domain_pattern

        owl_pattern += "     \t\t\t</owl:unionOf>\n" + \
                       "     \t\t</owl:Class>\n" + \
                       "     \t</rdfs:domain>\n" + \
                       "     \t<rdfs:range>\n" + \
                       "     \t\t<owl:Class>\n" + \
                       "     \t\t\t<owl:unionOf rdf:parseType=\"Collection\">\n"

        range_pattern = ""

        for item in rdfs_range:
            item = item.replace(' ', '_')
            range_pattern += "     \t\t\t\t<owl:Class rdf:about=\"#{0}\"/>\n".format(item)

        owl_pattern += range_pattern

        owl_pattern += "     \t\t\t</owl:unionOf>\n" + \
                       "     \t\t</owl:Class>\n" + \
                       "     \t</rdfs:range>\n" + \
                       "     </owl:ObjectProperty>\n"

        return "\n" + owl_pattern + "\n"

    def to_owl_string(self):

        # properties
        # unions
        # restrictions
        # classes etc.

        owl_header = "     <!--" + \
                     "\n     ///////////////////////////////////////////////////////////////////////////////////////" + \
                     "\n     //" + \
                     "\n     // Object Properties" + \
                     "\n     //" + \
                     "\n     ///////////////////////////////////////////////////////////////////////////////////////" + \
                     "\n     -->\n\n\n\n\n"

        if len(self.__cp_relations) > 0 or len(self.__unions) > 0 or len(self.__restrictions) > 0 or len(
                self.__cpvd_relations) > 0 or len(self.__cpvi_relations) > 0:
            self.__content += owl_header

        self.__content += self.__encode_all_unions()
        # self.__content += self.__encode_all_restrictions()
        # UPD: restrictions

        # CP
        for relation in self.__cp_relations:
            class_name = relation[0]
            class_property = relation[1]
            self.__content += self.__encode_cp_relationship(class_name, class_property)

        # CPVD
        for relation in self.__cpvd_relations:
            class_name = relation[0]
            class_property = relation[1]
            property_value = relation[2]
            self.__content += self.__encode_cpvd_relationship(class_name, class_property, property_value)

        # CPVI
        for relation in self.__cpvi_relations:
            class_name = relation[0]
            class_property = relation[1]
            property_value = relation[2]
            self.__content += self.__encode_cpvi_relationship(class_name, class_property, property_value)

        self.__content += self.__encode_classes()

        self.__content += '\n\n'

        # CSC
        for item in self.__csc_relations:
            self.__content += self.__encode_csc_relationship(item[0], item[1])

        # CI
        for relation in self.__ci_relations:
            concept = relation[0]
            instance = relation[1]
            self.__content += self.__encode_ci_relationship(concept, instance)

        copyrights = "<!-- Generated by the RTA https://github.com/UmbrellaBurns/RTA -->"

        return self.__content + "\n</rdf:RDF>" + '\n\n\n' + copyrights

    def save_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(self.to_owl_string())
