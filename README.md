# LiniMuda website

Code for site at: https://linimuda.id


## Getting started

Make sure Python 3.5 or higher is installed on your system.
Open `webapps` directory in a command prompt, then:

1. Install the software, check, then do migraton:
   ```
   pip install -r requirements.txt
   python manage.py check
   python manage.py 
   ```

2. Run the development server:
   ```
   python manage.py runserver
   ```

3. Create an admin user with:

```
python manage.py createsuperuser
```
and follow the instruction on terminal.

4. Go to http://localhost:8000/ in your browser, or http://localhost:8000/admin/
   to log in and get to work!

## Documentation links

* To customize the content, design, and features of the site see
  [CodeRed CMS](https://docs.coderedcorp.com/cms/).

* For deeper customization of backend code see
  [Wagtail](http://docs.wagtail.io/) and
  [Django](https://docs.djangoproject.com/).

* For HTML template design see [Bootstrap](https://getbootstrap.com/).

---

Made with ♥ using [Wagtail](https://wagtail.io/) +
[CodeRed CMS](https://www.coderedcorp.com/cms/)
