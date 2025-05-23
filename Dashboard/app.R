library(shiny)
library(dplyr)
library(ggplot2)
library(DT)

# Ensure stock_data is loaded and the Date column is properly formatted
stock_data = read.csv("stocks.csv")
predictions = read.csv("predictions2.csv")


stock_data <- stock_data %>%
  mutate(date = as.Date(date,format="%Y-%m-%d")) %>%
  filter(!is.na(date))

predictions = predictions %>%
  mutate(date = as.Date(date,format="%Y-%m-%d"))

print(range(stock_data$date, na.rm = TRUE))
print(range(predictions$date, na.rm = TRUE))

# Handle any potential NAs in Date column

# Define UI
ui <- fluidPage(
  titlePanel("Stock Analysis and Prediction App"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("company", "Select Company:", 
                  choices = unique(stock_data$entity)),
      uiOutput("date_slider")
    ),
    
    mainPanel(
      plotOutput("stock_chart"),
      DTOutput("prediction_table")
    )
  )
)

# Define server logic
server <- function(input, output, session) {
  
  filtered_data <- reactive({
    req(input$company)
    stock_data %>%
      filter(entity == input$company)
  })
  
  filtered_predictions = reactive({
    req(input$company)
    predictions %>% filter(entity == input$company)
  })
  
  observe({
    data <- filtered_predictions()
    if (nrow(data) > 0 && !all(is.na(data$date))) {
      date_range <- range(data$date, na.rm = TRUE)
    } else {
      date_range <- range(predictions$date, na.rm = TRUE)
    }
    
    #print(paste("Date range for", input$company, ":", date_range[1], "to", date_range[2]))
    
    updateSliderInput(session, "date",
                      min = date_range[1],
                      max = date_range[2],
                      value = min(date_range[2], max(date_range[1], median(date_range))))
  })
    
    output$date_slider <- renderUI({
      sliderInput("date", "Select Date:",
                  min = as.Date("2000-01-01"),  # Set a default range
                  max = as.Date("2100-12-31"),  # that will be updated
                  value = as.Date("2000-01-01"),
                  timeFormat = "%d/%m/%Y",
                  animate = TRUE,
                  step = 1)
    })
    
    company_colors <- c(
      "GME" = "#663333",
      "WING" = "#215622",
      "NVDA" = "#232255",
      "DOGE" = "#666633"
    )
  
  
  output$stock_chart <- renderPlot({
    req(input$company, input$date)
    
    data <- filtered_data()
    #selected_date <- data %>% filter(date == input$date)
    
    # CHANGE: Ensure there's data to plot
    if (nrow(data) == 0) {
      return(ggplot() + 
               ggtitle("No data available for this company") + 
               theme_minimal())
    }
    
    selected_date <- data %>% 
      filter(date == as.Date(input$date)) %>%
      slice(1)
    
    ggplot(data, aes(x = date, y = close)) +
      geom_line(color = company_colors[input$company]) +
      geom_vline(xintercept = as.Date(input$date),
                 color = "blue", linetype = "dashed") +
      geom_point(data = selected_date,
                 aes(x = date, y = close),
                 color = "black", size = 3) +
      labs(title = paste("Stock Price for", input$company),
           x = "Date", y = "Closing Price") +
      theme_minimal()
  })
  
  output$prediction_table <- renderDT({
    req(input$company, input$date)
    
    filtered_preds = filtered_predictions()
    
    day_preds = filtered_preds %>%
      filter(date == as.Date(input$date),
             entity == (input$company))
    
    #filtered_predictions <- filtered_predictions %>%
    #  filter(entity == (input$company),
    #         date == as.Date(input$date))
    
    if (nrow(day_preds) == 0) {
      return(data.frame(Message = "No predictions available for this date and company", stringsAsFactors = FALSE))
    }
    
    day_preds %>%
      select(date, Day1, Day2, Day3, Day4, Day5)
  })
  
  # output$debug_output <- renderPrint({
  #   cat("Selected company:", input$company, "\n")
  #   cat("Date range in filtered predictions:\n")
  #   print(range(filtered_predictions()$date, na.rm = TRUE))
  #   cat("Current slider value:", input$date, "\n")
  # })
}

# Run the application
shinyApp(ui = ui, server = server)
