from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import Article


# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')


def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()

    param = {
        "date": date,
        "news": news
    }

    return render(request, 'all-news/today-news.html', param)


def convert_dates(dates):
    # Function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', "Sunday"]

    # Returning the actual day of the week
    day = days[day_number]
    return day


def past_days_news(request, past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date": date, "news": news})


def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f'{search_term}'

        param = {
            "message": message,
            "articles": searched_articles
        }

        return render(request, 'all-news/search.html', param)
    else:
        message = "you have not searched for any message"
        return render(request, 'all-news/search.html', {"message": message})


def article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "all-news/articles.html", {"article": article})
