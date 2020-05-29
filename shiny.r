
pkgs <- c("data.table", "dplyr", "shiny", "DT", "shinydashboard", "stringr")

ins_pkgs = pkgs[!( pkgs %in% installed.packages()[, "Package"] )]
if(length(ins_pkgs)) install.packages(ins_pkgs)
for(pkg in pkgs) library(pkg, character.only = TRUE)

# https://htmlcolorcodes.com/color-chart/

setwd("C:/Users/10905310/PycharmProjects/aws")

####################################################################################################

all_reports <- dir("./data/report/", full.names = T)
transcript_path <- all_reports[grepl(x = all_reports, pattern = ".csv")]

# read transcript
transcript_path <- all_reports[grepl(x = all_reports, pattern = "report_")] %>% sort(x = .) %>% tail(x = ., n = 1)
transcript <- fread(input = transcript_path, header = T)
transcript <- transcript %>% 
  select(-V1) %>% 
  mutate(
    comment = gsub(x = comment, pattern = "\\$", replacement = "")
  )
segment <- array(0, nrow(transcript))
for(i in 1:nrow(transcript)){
  if(i == 1) temp = 0
  if(i != 1){
    if(transcript$speaker[i] == transcript$speaker[i-1]) segment[i] = temp
    if(transcript$speaker[i] != transcript$speaker[i-1]){
      temp = temp + 1
      segment[i] = temp
    }
  }
}
transcript <- transcript %>% 
  mutate(
    segment = segment
  ) %>% 
  group_by(speaker, segment) %>% 
  summarise(
    start_time = head(start_time, 1), 
    end_time = tail(end_time, 1), 
    comment = paste0(comment, collapse = " ")
  ) %>% 
  ungroup() %>% 
  arrange(start_time) %>% 
  select(-segment)

# read keyword
keyword_path <- all_reports[grepl(x = all_reports, pattern = "keyword")] %>% sort(x = .) %>% tail(x = ., n = 1)
keywords <- read.csv(file = keyword_path, header = F)
keywords <- keywords %>% 
  # arrange(V1) %>% 
  mutate(
    V1 = gsub(x = V1, pattern = "\\$", replacement = ""), 
    V2 = round(V2, 2)
  )
confidence <<- keywords$V2
keywords <<- keywords$V1

####################################################################################################

highlight <- function(text, search, color = "red"){
  text %>% 
    stringr::str_replace_all(
      string = ., 
      pattern = search, 
      replacement = paste0('<span style="background-color:', color, '">', search, '</span>')
    )
}

counts <- function(text, search, init = ""){
  if(length(search) == 0) return(init)
  temp = stringr::str_count(string = text, pattern = search)
  paste0("appears ", temp, " times")
}

confds <- function(search, init = ""){
  if(length(search) == 0) return(init)
  temp = confidence[search == keywords]
  paste0("confidence: ", temp)
}

highlight_all <- function(transcript, keywords){
  if(length(keywords) == 0){
    result = transcript
  }
  if(length(keywords) == 1){
    result <- transcript %>%
      mutate(
        comment = sapply(X = comment, FUN = highlight, search = keywords[1], color = "#EC7063")
      )
  }
  if(length(keywords) == 2){
    result <- transcript %>%
      mutate(
        comment = sapply(X = comment, FUN = highlight, search = keywords[1], color = "#EC7063"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[2], color = "#EB984E")
      )
  }
  if(length(keywords) == 3){
    result <- transcript %>%
      mutate(
        comment = sapply(X = comment, FUN = highlight, search = keywords[1], color = "#EC7063"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[2], color = "#EB984E"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[3], color = "#45B39D")
      )
  }
  if(length(keywords) == 4){
    result <- transcript %>%
      mutate(
        comment = sapply(X = comment, FUN = highlight, search = keywords[1], color = "#EC7063"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[2], color = "#EB984E"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[3], color = "#45B39D"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[4], color = "#5DADE2")
      )
  }
  if(length(keywords) == 5){
    result <- transcript %>%
      mutate(
        comment = sapply(X = comment, FUN = highlight, search = keywords[1], color = "#EC7063"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[2], color = "#EB984E"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[3], color = "#45B39D"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[4], color = "#5DADE2"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[5], color = "#AF7AC5")
      )
  }
  if(length(keywords) == 6){
    result <- transcript %>%
      mutate(
        comment = sapply(X = comment, FUN = highlight, search = keywords[1], color = "#EC7063"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[2], color = "#EB984E"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[3], color = "#45B39D"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[4], color = "#5DADE2"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[5], color = "#AF7AC5"), 
        comment = sapply(X = comment, FUN = highlight, search = keywords[6], color = "#CACFD2")
      )
  }
  return(result)
}

color_speaker <- function(transcript){
  color_set <- c("#F9EBEA", "#F5EEF8", "#EAF2F8", "#E8F8F5", "#E9F7EF", "#FEF9E7", "#FDF2E9", "#FDFEFE", "#F4F6F6", "#EBEDEF")
  speaker_set <- unique(transcript$speaker)
  color_set <- color_set[1:length(speaker_set)]
  mapping <- data.frame(
    speaker = speaker_set, 
    color = color_set
  )
  mapping$speaker <- as.character(mapping$speaker)
  result <- left_join(transcript, mapping)
  color_set <- as.character(result$color)
  return(color_set)
}

####################################################################################################

tab_Report <- 
  tabItem(
    tabName = "tab_Report", 
    box(
      title = "Keywords", 
      status = "warning", 
      solidHeader = TRUE, 
      collapsible = TRUE, 
      collapsed = FALSE, 
      width = 12, 
      fluidRow(
        column(
          3, 
          sliderInput(
            inputId = "threshold", 
            label = "Choose Confidence Threshold: ", 
            min = range(confidence)[1], 
            max = range(confidence)[2], 
            value = range(confidence)[1]
          )
        ), 
        column(
          9, 
          uiOutput('keyword_list', placeholder = TRUE, inline = T)
        )
      ), 
      fluidRow(
        infoBoxOutput("keyword1", width = 4),
        infoBoxOutput("keyword2", width = 4), 
        infoBoxOutput("keyword3", width = 4), 
        infoBoxOutput("keyword4", width = 4), 
        infoBoxOutput("keyword5", width = 4), 
        infoBoxOutput("keyword6", width = 4)
      )
    ), 
    box(
      title = "Transcript", 
      status = "primary", 
      solidHeader = TRUE, 
      width = 12, 
      htmlOutput("some_text"), 
      # h3(HTML('<span style="background-color:red">spk</span>_0')), 
      DT::dataTableOutput("transcript")
    )
  )

ui <- dashboardPage(
  title = "Jiang-Jung-Dian", 
  dashboardHeader(
    title = "Jiang-Jung-Dian", 
    titleWidth = 250
  ), 
  dashboardSidebar(
    sidebarMenu(
      menuItem(
        "Report", tabName = "tab_Report", icon = icon("columns"), badgeLabel = "200528.001", badgeColor = "green"
      )
    ), 
    width = 250
  ), 
  dashboardBody(
    tags$head(
      tags$style(HTML(".main-sidebar { font-size: 16px; }"))
    ), 
    tags$head(
      tags$link(
        rel = "shortcut icon", 
        href = "https://image.flaticon.com/icons/svg/1277/1277753.svg", 
        type = "image/vnd.microsoft.icon"
      )
    ), 
    tabItems(
      # tabItem(tabName = "tab_Report", h2("tab_Report"))
      tab_Report
    )
  )
)

####################################################################################################

server <- function(input, output){
  output$keyword1 <- renderInfoBox({
    if(length(input$keywords) < 1){
      infoBox(
        title = "", 
        value = "", 
        icon = icon("dice-one"),
        color = "red", fill = TRUE
      )
    } else{
      infoBox(
        title = input$keywords[1], 
        subtitle = confds(search = input$keywords[1]), 
        value = counts(text = paste0(transcript$comment, collapse = " "), search = input$keywords[1], init = ""), 
        icon = icon("dice-one"),
        color = "red", fill = TRUE
      )
    }
  })
  output$keyword2 <- renderInfoBox({
    if(length(input$keywords) < 2){
      infoBox(
        title = "", 
        value = "", 
        icon = icon("dice-two"),
        color = "yellow", fill = TRUE
      )
    } else{
      infoBox(
        title = input$keywords[2], 
        subtitle = confds(search = input$keywords[2]), 
        value = counts(text = paste0(transcript$comment, collapse = " "), search = input$keywords[2], init = ""), 
        icon = icon("dice-two"),
        color = "yellow", fill = TRUE
      )
    }
  })
  output$keyword3 <- renderInfoBox({
    if(length(input$keywords) < 3){
      infoBox(
        title = "", 
        value = "", 
        icon = icon("dice-three"),
        color = "green", fill = TRUE
      )
    } else{
      infoBox(
        title = input$keywords[3], 
        subtitle = confds(search = input$keywords[3]), 
        value = counts(text = paste0(transcript$comment, collapse = " "), search = input$keywords[3], init = ""), 
        icon = icon("dice-three"),
        color = "green", fill = TRUE
      )
    }
  })
  output$keyword4<- renderInfoBox({
    if(length(input$keywords) < 4){
      infoBox(
        title = "", 
        value = "", 
        icon = icon("dice-four"),
        color = "blue", fill = TRUE
      )
    } else{
      infoBox(
        title = input$keywords[4], 
        subtitle = confds(search = input$keywords[4]), 
        value = counts(text = paste0(transcript$comment, collapse = " "), search = input$keywords[4], init = ""), 
        icon = icon("dice-four"),
        color = "blue", fill = TRUE
      )
    }
  })
  output$keyword5 <- renderInfoBox({
    if(length(input$keywords) < 5){
      infoBox(
        title = "", 
        value = "", 
        icon = icon("dice-five"),
        color = "purple", fill = TRUE
      )
    } else{
      infoBox(
        title = input$keywords[5], 
        subtitle = confds(search = input$keywords[5]), 
        value = counts(text = paste0(transcript$comment, collapse = " "), search = input$keywords[5], init = ""), 
        icon = icon("dice-five"),
        color = "purple", fill = TRUE
      )
    }
  })
  output$keyword6 <- renderInfoBox({
    if(length(input$keywords) < 6){
      infoBox(
        title = "", 
        value = "", 
        icon = icon("dice-six"),
        color = "black", fill = TRUE
      )
    } else{
      infoBox(
        title = input$keywords[6], 
        subtitle = confds(search = input$keywords[6]), 
        value = counts(text = paste0(transcript$comment, collapse = " "), search = input$keywords[6], init = ""), 
        icon = icon("dice-six"),
        color = "black", fill = TRUE
      )
    }
  })
  output$transcript <- DT::renderDataTable({
    temp <- highlight_all(transcript = transcript, keywords = input$keywords)
    temp <- DT::datatable(
      data = temp, 
      escape = F, 
      options = list(
        info = F,
        paging = F,
        searching = F,
        lengthChange = F,
        scrollY = 500
      )
    ) %>% 
      formatStyle(
        columns = 1:ncol(transcript),
        valueColumns = 0,
        backgroundColor = styleInterval(
          cuts = 1:(nrow(transcript)-1),
          values = color_speaker(transcript)
        )
      )
    return(temp)
  })
  output$keyword_list <- 
    renderUI(
      {
        tmp <- keywords[confidence >= input$threshold]
        selectizeInput(
          inputId = "keywords", 
          label = "Select Keywords: (at most 6)", 
          choices = tmp, 
          multiple = T, 
          options = list(maxItems = 6)
        )
      }
    )
}

####################################################################################################

options(browser = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
runApp(list(ui = ui, server = server), launch.browser = TRUE)
