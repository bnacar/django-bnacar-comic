from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import Episode, Series, Tag

class ComicTagTests(TestCase):
    def test_basic_tag(self):
        tag1 = Tag(name='First Tag')
        tag1.save()
        self.assertEqual(tag1.slug, 'first-tag')
        tagOne = Tag(name='first tag')
        # there should be no collisions
        with self.assertRaises(IntegrityError) as e:
             tagOne.save()

class ComicSeriesTests(TestCase):
    def test_basic_series(self):
        series1 = Series(title='Test Series', blurb='beep boop')
        series1.save()
        self.assertEqual(series1.slug, 'woopwoopwoop')
        series1.slug = 'test-series'
        series1.save()
        url1 = reverse('comic:index', args=('test-series',))
        res1 = self.client.get(url1)
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, 'Test Series')
        self.assertContains(res1, 'beep boop')
        url2 = reverse('comic:index', args=('fake-series',))
        res2 = self.client.get(url2)
        self.assertEqual(res2.status_code, 404)
        seriesOne = Series(title='Another Test Series', slug='test-series')
        with self.assertRaises(IntegrityError) as e:
             seriesOne.save()

class ComicEpisodeTests(TestCase):
    def test_basic_episode(self):
        tag4 = Tag(name='Fourth Tag')
        tag5 = Tag(name='Fifth Tag')
        tag6 = Tag(name='Sixth Tag')
        tag4.save()
        tag5.save()
        tag6.save()
        series2 = Series(title='Test Series 2', slug='test2', blurb='something or other')
        series2.save()
        episode2_1 = Episode(num=1, comic=series2, imgFile='/tmp/lolcat.jpg')
        episode2_2 = Episode(num=2, comic=series2, imgFile='/tmp/loldog.jpg', notes='woof')
        episode2_4 = Episode(num=4, comic=series2, imgFile='/tmp/lolol.jpg', transcript='all your base are belong to us')
        episode2_1.save()
        episode2_1.tags.set([tag4])
        episode2_2.save()
        episode2_2.tags.set([tag5])
        episode2_4.save()
        episode2_4.tags.set([tag4, tag5])

        url_index = reverse('comic:index', args=('test2',))
        url1 = reverse('comic:episode', args=('test2', 1))
        url2 = reverse('comic:episode', args=('test2', 2))
        url3 = reverse('comic:episode', args=('test2', 3))
        url4 = reverse('comic:episode', args=('test2', 4))

        res_index = self.client.get(url_index)
        self.assertEqual(res_index.status_code, 200)
        self.assertContains(res_index, 'Fourth Tag')
        self.assertContains(res_index, 'Fifth Tag')
        self.assertNotContains(res_index, 'Sixth Tag')

        res1 = self.client.get(url1)
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, 'Test Series 2')
        self.assertContains(res1, '/tmp/lolcat.jpg')
        self.assertContains(res1, 'Fourth Tag')
        self.assertNotContains(res1, url1)
        self.assertContains(res1, url2) # link to "next"
        self.assertNotContains(res1, url3)
        self.assertContains(res1, url4) # link to "last"
        self.assertNotContains(res1, 'Fifth Tag')
        
        res2 = self.client.get(url2)
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, 'Test Series 2')
        self.assertContains(res2, '/tmp/loldog.jpg')
        self.assertNotContains(res2, 'Fourth Tag')
        self.assertContains(res2, 'Fifth Tag')
        self.assertContains(res2, url1) # link to "first", "prev"
        self.assertNotContains(res2, url2)
        self.assertNotContains(res2, url3)
        self.assertContains(res2, url4) # link to "next", "last"
        self.assertNotContains(res2, '/tmp/lolcat.jpg')
        self.assertNotContains(res2, 'all your base are belong to us')
        
        res3 = self.client.get(url3)
        self.assertEqual(res3.status_code, 404)
        
        res4 = self.client.get(url4)
        self.assertEqual(res4.status_code, 200)
        self.assertContains(res4, 'Test Series 2')
        self.assertContains(res4, '/tmp/lolol.jpg')
        self.assertContains(res4, 'all your base are belong to us')
        self.assertContains(res4, 'Fourth Tag')
        self.assertContains(res4, 'Fifth Tag')
        self.assertContains(res4, url1) # link to "first"
        self.assertContains(res4, url2) # link to "prev"
        self.assertNotContains(res4, url3)
        self.assertNotContains(res4, url4)
