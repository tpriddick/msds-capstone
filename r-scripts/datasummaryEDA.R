# Capstone EDA
library(tidyverse)
library(DBI)
library(RPostgres)

# Connecting to SQL Database
con = dbConnect(
  RPostgres::Postgres(),
  dbname = 'railway',
  host = 'roundhouse.proxy.rlwy.net',
  port = 44826,
  user = 'postgres',
  password = 'WjValpnjgoYyLCVqoPrZhiSbVwdbgbUh'
)

# Pull in posts table
posts = tbl(con, sql("SELECT * FROM posts"))
posts

# Pull in stock information
gme = read.csv("/Users/leotyler/Downloads/GME.csv")
nvda = read.csv("/Users/leotyler/Downloads/NVDA.csv")
wing = read.csv("/Users/leotyler/Downloads/WING.csv")
dogecoin =read.csv2("/Users/leotyler/Downloads/Dogecoin.csv")

ggplot(gme,aes(x=as.Date(Date),y=Close)) +
  geom_line(color='#FD0000',size = 1.25) +
  scale_x_date(date_breaks = '1 month', date_minor_breaks = '1 month',
               date_labels = "%b '%y") +
  theme_minimal() +
  theme(
    title = element_text(size = 20),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(size = 10)
    )+
  labs(
    title = 'GameStop Closing Stock Prices from Jan 2020 through Jan 2022',
    x = 'Date',
    y = 'Closing Price ($ Per Share)'
  )

ggsave('gmestocks.png')

ggplot(wing,aes(x=as.Date(Date),y=Close)) +
  geom_line(color='#066A36',size = 1.25) +
  scale_x_date(date_breaks = '1 month', date_minor_breaks = '1 month',
               date_labels = "%b '%y") +
  theme_minimal() +
  theme(
    title = element_text(size = 20),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(size = 10)
    )+
  labs(
    title = 'Wingstop Closing Stock Prices from Jul 2021 through Jun 2024',
    x = 'Date',
    y = 'Closing Price ($ Per Share)'
  )

ggsave('wingstocks.png')

ggplot(nvda,aes(x=as.Date(Date),y=Close)) +
  geom_line(color='#76B900',size = 1.25) +
  scale_x_date(date_breaks = '1 month', date_minor_breaks = '1 month',
               date_labels = "%b '%y") +
  theme_minimal() +
  theme(
    title = element_text(size = 20),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(size = 10)
        )+
  labs(
    title = 'Nvidia Closing Stock Prices from Jul 2022 through Jun 2024',
    x = 'Date',
    y = 'Closing Price ($ Per Share)'
  )

ggsave('nvdastocks.png')

ggplot(dogecoin,aes(x=as.Date(timestamp),y=as.numeric(close))) +
  geom_line(color='#CB9800',size = 1.25) +
  scale_x_date(date_breaks = '1 month', date_minor_breaks = '1 month',
               date_labels = "%b '%y") +
  theme_minimal() +
  theme(
    title = element_text(size = 20),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(size = 10)
        )+
  labs(
    title = 'Dogecoin Closing Stock Prices from Dec 2021 through Jan 2023',
    x = 'Date',
    y = 'Closing Price ($ Per Share)'
  )

ggsave('dogecoinstocks.png')

# Closing stock prices vs likes
likeSumm = posts %>%
  mutate(date_posted = as.Date(date_posted)) %>%
  group_by(date_posted) %>%
  summarize(avg_likes = mean(likes))

likeSumm = as.data.frame(likeSumm)

gme = gme %>%
  mutate(Date = as.Date(Date))

gme %>%
  inner_join(likeSumm, join_by(Date == date_posted)) %>%
  ggplot(aes(x = Date, y = avg_likes, size = Close, color = Close)) +
  geom_point() +
  theme_bw() +
  labs(
    title = 'Average Likes per Post Compared to Closing Price',
    subtitle = 'GME Stock, January to March 2020',
    y = 'Average Likes per Post',
    color = 'Closing Price'
  ) +
  theme(
    title = element_text(size = 20),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(size = 13),
    axis.text.y = element_text(size = 13)
  ) +
  scale_color_viridis_c(option = 'magma') +
  guides(size = FALSE)

ggsave('avg_likes.png')

gme %>%
  inner_join(likeSumm, join_by(Date == date_posted)) %>%
  ggplot(aes(x = avg_likes, y = Close)) +
  geom_point(color='cyan4',size = 3) +
  labs(
    title = 'Closing Price per Share vs Average Likes per Post',
    subtitle = 'GME Stock, January to March 2020',
    x = 'Average Likes per Post',
    y = 'Closing Price per Share in $',
    color = 'Closing Price per Share in $'
  ) +
  theme(
    title = element_text(size = 20),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(size = 13),
    axis.text.y = element_text(size = 13)
  ) +
  scale_color_viridis_c(option = 'magma') +
  guides(size = FALSE)

ggsave('close_v_likes.png')

