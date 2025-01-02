class DocumentationGenerator:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
    def generate_documentation(self, config, data):
        print("Types data:", data.get('types', []))  # Debug print
        print("Docs data:", data.get('docs', []))    # Debug print

        # Load all card templates
        api_card_template = self.env.get_template('components/api_card.html')
        type_card_template = self.env.get_template('components/type_card.html')
        doc_card_template = self.env.get_template('components/doc_card.html')
        
        # Generate content for each section
        api_cards = ''.join([
            api_card_template.render(item=api_item, **config)
            for api_item in data.get('apis', [])
        ])
        
        type_cards = ''.join([
            type_card_template.render(item=type_item, **config)
            for type_item in data.get('types', [])
        ])
        
        doc_cards = ''.join([
            doc_card_template.render(item=doc_item, **config)
            for doc_item in data.get('docs', [])
        ])
        
        # Render main template with all content
        template = self.env.get_template('cacao_template.html')
        return template.render(
            API_CARD_CONTENT=api_cards,
            TYPES_CARD_CONTENT=type_cards,
            DOCS_CARD_CONTENT=doc_cards,
        ])
            **config
        )

        
        # Render main template with all content
        template = self.env.get_template('cacao_template.html')
        return template.render(
            API_CARD_CONTENT=api_cards,
            TYPES_CARD_CONTENT=type_cards,
            DOCS_CARD_CONTENT=doc_cards,
            **config
        )
