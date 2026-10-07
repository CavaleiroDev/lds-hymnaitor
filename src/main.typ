#set text(size: 17pt)
#show heading: set align(center)
#set list(marker: [])
#set enum( // altera a aparencia de toda a lista numerada '0.' para não exibir indicador numerico. Isso é feito para que nos casos raros onde a música possui uma ponte (bridge) a visibilidade não fique incoerente com a do site
  numbering: n => if n == 0 { "   " } else { str(n) + "." }
)

#set page(footer: context[#set align(center); #counter(page).display()], margin: (
  top: 40pt,

))

#let indicador_E(txt) = {
  set align(top)
  set align(left)
  txt
}

#let indicador_D(txt) = {
  set align(top)
  set align(right)
  txt
}

#let titulo(txt) = {
  set align(top)
  set align(center)
  txt
}

#let info-musica(txt) = {
  set align(bottom)
  set text(size: 11pt)
  txt
}

//--------

#let columns_data = json("../dados/columns.json")
#let hinos_list = json("../dados/hinos.json")

#let pages_to_manualy_break = ( // determina quais hinos precisam de uma quebra de página antes para que hinos vazados fiquem sempre em páginas ímpares
  1004,
  //1011,
  //1013,
  1021,
  1033,
  1052,
  1064,
  1069
)

#let pages_to_not_break = ( // determina quais hinos não devem quebrar de página no final
  1005,
  1011,
  1064,
)


#for h_path in hinos_list {
  let hino = json(h_path.at(1))
  let pagina_inicio_do_hino = 0

  for p in pages_to_manualy_break { // gera quebras de página manuais
    if hino.id == str(p){
      pagebreak()
      break
    }
  }

  context { // gera o número do hino na esquerda ou direita dependendo da página
    let pagina = counter(page).get().at(0)

    if calc.odd(pagina){ // ímpar
      indicador_E[*#hino.id*]
    }else{ // par
      indicador_D[*#hino.id*]
    }
  }

  [= #titulo[*#hino.name*] #label("inicio_musica"+hino.id) ] // gera o título do hino
  
  linebreak()

  columns(columns_data.at(hino.id))[ // pega e aplica o valor de em  quantas colunas separar o conteudo

    #for s in hino.content{ // gera as estrofes do hino
      if s.tipo == "stanza"{
        let n = s.number
        enum(enum.item(n)[#s.text]) // se der problema aqui, provavelmente é culpa de algum .json que está mal configurado (com valor não numerico onde era para ser numero)
      }else if s.tipo == "chorus"{
        emph[- - #s.text]
      }
    }

    #place( // coloca as informação da música no documento
      bottom,
      scope: "parent",
      float: true,
      
      info-musica[ // formata as informações da música
      #for c in hino.citation { // gera os créditos e informações
        [#c #linebreak()]
        }
      
      #hino.scriptures.at(0) | #hino.scriptures.at(1) #label("fim_musica"+hino.id)
      /* // como sei que todos os hinos só tem duas escrituras, e para ter somente um separador ao invés de ao final de cada escritura, vou manualmente aplicá-los
      #for s in hino.scriptures { // gera as escrituras usadas de base
        [#s #linebreak()]
        }*/
      ]
    )
  ]
  
  context { // gera o número do hino na esquerda ou direita dependendo da página
    let p_inicio = locate(label("inicio_musica"+hino.id)).page()
    let p_fim = locate(label("fim_musica"+hino.id)).page()

    if p_inicio != p_fim{ // Detecta se o trecho da musica vazou da pagina
      //[ESTÁ MÚSICA ESTÁ QUEBRANDO A PÁGINA]
      if calc.odd(p_inicio){ // ímpar 
        //[TUDO OK]
      }else{ // par
        //[TEM QUE DAR PAGEBREAK antes desse hino!!!]
        // 
        // a ideia era com base nisso dar break em paginas que estivessem vazando para a folha seguinte, assim não haveria o desconforto de ter de virar de página no meio do hino. porém essa implementação automática não funcionou e tive que fazer isso manualmente lá encima do arquivo.
      }
    }
  }

  let breakpage = true
  for p in pages_to_not_break { // gera quebras de página manuais
    if hino.id == str(p){
      breakpage = false
      break
    }
  }
  if breakpage {
    pagebreak() // pula para a próxima página. assim não há corte de página entre hinos
  }
}