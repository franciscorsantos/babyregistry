from app import app
from models import db, Item, Presente

def seed_database():
    with app.app_context():
        db.create_all()

        if Item.query.count() == 0:
            items_data = [
            {
                "nome": "Fralda P",
                "categoria": "Higiene",
                "valor": 65.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_802958-MLA104909902718_012026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda P",
                "categoria": "Higiene",
                "valor": 65.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_885242-MLA99452807958_112025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda P",
                "categoria": "Higiene",
                "valor": 65.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_900853-MLB110512922111_042026-F-kit-2-pacotes-fralda-huggies-tripla-protecao-tam-p-76-un.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda P",
                "categoria": "Higiene",
                "valor": 65.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_899216-MLA99840351095_112025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda M",
                "categoria": "Higiene",
                "valor": 149.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_894429-MLA99934926577_112025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda M",
                "categoria": "Higiene",
                "valor": 149.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_878597-MLA99452088202_112025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda M",
                "categoria": "Higiene",
                "valor": 149.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_729959-MLA99437189922_112025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda M",
                "categoria": "Higiene",
                "valor": 149.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_699987-MLB110991165958_052026-F-kit-2-pacotes-fraldas-galinha-pintadinha-g-babysec-ultrasec.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda G",
                "categoria": "Higiene",
                "valor": 102.21,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_995072-MLA85757844717_062025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda G",
                "categoria": "Higiene",
                "valor": 102.21,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_697162-MLA99700990440_122025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda G",
                "categoria": "Higiene",
                "valor": 102.21,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_699987-MLB110991165958_052026-F-kit-2-pacotes-fraldas-galinha-pintadinha-g-babysec-ultrasec.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda G",
                "categoria": "Higiene",
                "valor": 102.21,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_800100-MLA99924950787_112025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Lenços Umedecidos",
                "categoria": "Higiene",
                "valor": 66.78,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_881068-MLA100185992729_122025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Lenços Umedecidos",
                "categoria": "Higiene",
                "valor": 66.78,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_753827-MLA80015367155_102024-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Lenços Umedecidos",
                "categoria": "Higiene",
                "valor": 66.78,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_733094-MLA117672173051_092026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Pomada Bepantol Baby 120g",
                "categoria": "Higiene",
                "valor": 59.90,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_929027-MLA105016515224_012026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Sabonete Líquido p/ Recém Nascido",
                "categoria": "Higiene",
                "valor": 44.50,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_997281-MLU75858805097_042024-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Sabonete Líquido p/ Recém Nascido",
                "categoria": "Higiene",
                "valor": 44.50,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_700458-MLB88513091389_072025-F-kit-johnsons-rescen-nascido-sabonete-e-locao-hidratante.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Kit Higiene E Saúde",
                "categoria": "Higiene",
                "valor": 256.49,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_851354-MLB107302901148_032026-F-enxoval-para-recemnascido-20-itens-kit-higiene-e-saude.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Toalha De Banho",
                "categoria": "Banho",
                "valor": 45.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_716713-MLB100661070523_122025-F-toalha-de-banho-forrada-com-fralda-dupla-face-bordada.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Toalha De Banho",
                "categoria": "Banho",
                "valor": 45.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_782009-MLA111395494951_052026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda de Pano",
                "categoria": "Cuidados",
                "valor": 67.51,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_690228-MLA111899315945_052026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda de Pano",
                "categoria": "Cuidados",
                "valor": 67.51,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_928280-MLB90887788794_082025-F-kit-05-fralda-pano-bordada-com-bainha-70x68-loupiot.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda de Pano",
                "categoria": "Cuidados",
                "valor": 67.51,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_710334-MLB101297344158_122025-F-kit-5-fraldas-de-pano-luxo-turma-da-mnica-baby.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Fralda de Pano",
                "categoria": "Cuidados",
                "valor": 67.51,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_690228-MLA111899315945_052026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Cueiro de Algodão",
                "categoria": "Quarto",
                "valor": 73.99,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_799234-MLB113103210433_062026-F-kit-3-cueiro-papi-100-algodao-flanelado-manta-bebe-enxoval.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Cueiro de Algodão",
                "categoria": "Quarto",
                "valor": 73.99,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_821146-MLB115487968306_082026-F-kit-cueiro-manta-estampado-80x50-algodo-confortavel-beb.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Body Manga Curta",
                "categoria": "Roupas",
                "valor": 49.99,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_917517-MLB108496784585_032026-F-kit-com-2-body-manga-curta-em-cotton-algodao-premium.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Body Manga Curta",
                "categoria": "Roupas",
                "valor": 49.99,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_987581-MLA115295428272_082026-F-kit-de-body-carters-5-pecas.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Body Manga Curta",
                "categoria": "Roupas",
                "valor": 49.99,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_965030-MLB116511986120_092026-F-kit-body-carters-original-pack-manga-curta-menino.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Body Manga Longa",
                "categoria": "Roupas",
                "valor": 49.99,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_925218-MLB89839471410_082025-F-kit-3-body-beb-liso-manga-longa-100-algodo-antialergico.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Mijões com e sem pé",
                "categoria": "Roupas",
                "valor": 55.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_799270-MLB95715142743_102025-F-kit-3-conjunto-body-e-mijo-beb-menino-cicinho.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Mijões com e sem pé",
                "categoria": "Roupas",
                "valor": 55.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_690251-MLB110422364850_052026-F-kit-5-mijo-beb-100-algodo-culote-menino-menina-rn-ao-g.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Mijões com e sem pé",
                "categoria": "Roupas",
                "valor": 55.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_772269-MLA109450491914_042026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Mijões com e sem pé",
                "categoria": "Roupas",
                "valor": 55.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_994464-MLB116756392623_082026-F-body-bebe-e-mijao-vira-pe-3-conjuntos-malha-canelada-6-pcs.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Toucas e Luvas",
                "categoria": "Roupas",
                "valor": 25.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_880525-MLB111188704191_052026-F-kit-2-touca-e-2-luva-para-bebe-recem-nascido-100-algodao.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Toucas e Luvas",
                "categoria": "Roupas",
                "valor": 25.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_936783-MLB97249458657_112025-F-kit-3-toucas-bebe-rn-com-luvas-algodao-canelado-premium.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Toucas e Luvas",
                "categoria": "Roupas",
                "valor": 25.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_955862-MLB79007218159_092024-F-kit-6pc-luva-beb-touca-3-luvinhas-e-3-gorros-recem-nascido.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Toucas e Luvas",
                "categoria": "Roupas",
                "valor": 25.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_612111-MLB117717368539_092026-F-kit-3-toucas-bebe-rn-com-luvas-algodao-canelado-premium.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Meias",
                "categoria": "Roupas",
                "valor": 30.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_769894-MLB84513382213_052025-F-kit-6-meias-kit-6-luvinhas-rnascido-algodo-meninos-macio.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Meias",
                "categoria": "Roupas",
                "valor": 30.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_757325-MLB111962788884_062026-F-kit-12-pares-de-meias-recem-nascido-menino-menina-enxoval.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Meias",
                "categoria": "Roupas",
                "valor": 30.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_741405-MLB108803966870_032026-F-kit-16-pares-de-meias-rn-saida-maternidade-enxoval-0a9-meses.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Meias",
                "categoria": "Roupas",
                "valor": 30.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_664437-MLB115481686011_082026-F-kit-7-pares-meia-bebe-todo-dia-rn-duck-menino-menina-algodao.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Trocador De Fralda",
                "categoria": "Quarto",
                "valor": 65.00,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_729322-MLA104702889196_012026-F.webp",
                "status": "disponivel",
                "destaque": False
            },
                # --- ALIMENTAÇÃO E AMAMENTAÇÃO ---
            {
                "nome": "Almofada de Amamentação",
                "categoria": "Amamentação",
                "valor": 63.36,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_920796-MLA106909901542_022026-F.webp",
                "status": "disponivel",
                "destaque": True
            },
            {
                "nome": "Kit Mamadeiras Anticólica",
                "categoria": "Alimentação",
                "valor": 214.90,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_939756-MLA95504085898_102025-F.webp",
                "status": "disponivel",
                "destaque": False
            },
            # --- ROUPAS (Cobertura e Frio) ---
            {
                "nome": "Macacão Longo com Zíper",
                "categoria": "Roupas",
                "valor": 79.90,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_691057-MLB116197160149_082026-F-macacao-bebe-longo-com-ziper-algodao-canelado-menino-menina.webp",
                "status": "disponivel",
                "destaque": False
            },
            {
                "nome": "Macacão Longo com Zíper",
                "categoria": "Roupas",
                "valor": 79.90,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_917497-MLB116660641663_082026-F-macacao-bebe-menino-menina-100-algodao-longo-ziper-virape.webp",
                "status": "disponivel",
                "destaque": False
            },
            # --- PASSEIO ---
            {
                "nome": "Bolsa Maternidade Térmica",
                "categoria": "Passeio",
                "valor": 229.90,
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_672969-MLB117885108239_092026-F-kit-de-bolsa-maternidade-5-pecas-mochila-termica-trocador.webp",
                "status": "disponivel",
                "destaque": True
            },
            {
                "nome": "Carrinho De Bebe Com Bebe Conforto E Base (Cota Solidária)",
                "categoria": "Passeio",
                "valor": 1609.08, 
                "imagem_url": "https://http2.mlstatic.com/D_NQ_NP_2X_810914-MLB118303599487_092026-F-carrinho-de-bebe-com-bebe-conforto-e-base-ivy-g22-black.webp",
                "status": "disponivel",
                "destaque": True
            }
            ]

            for item_info in items_data:
                item = Item(**item_info)
                db.session.add(item)
            
            db.session.commit()
            print("Itens cadastrados com sucesso!")
"""        # Seed sample approved message for the gifted item
        gifted_item = Item.query.filter_by(status='presenteado').first()
        if gifted_item and Presente.query.count() == 0:
            presente_exemplo = Presente(
                item_id=gifted_item.id,
                nome_convidado="Tia Dayse",
                mensagem="Que essa mantinha aqueça o seu bebê com todo o nosso amor e carinho! Mal podemos esperar para conhecer esse anjinho.",
                valor=gifted_item.valor,
                mp_payment_id="SIM-100200300",
                status_pagamento="approved"
            )
            db.session.add(presente_exemplo)
            db.session.commit()
            print("Recado inicial de presente cadastrado com sucesso!")
"""

if __name__ == "__main__":
    seed_database()
