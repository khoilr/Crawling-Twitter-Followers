# Crawler

This crawler use [`selenium`](https://www.seleniumhq.org/) to crawl the web.

Your account must set language to **English** and **English (United States)** in your browser.

Make sure Chrome is installed in your computer.

> :warning: **2-step verification is not supported**, so you need to **disable it**.
>
> **Note:** We don't collect any your information.

## Twitter Crawler

This module have two main features:

- Crawl followings of a Twitter user.
- Crawl followers of a Twitter user.

### `TwitterCrawler(account: dict)`

- `account`: A dict contains `username`, `password` and `email` for suspended login activity.

Example:

```python
account = {
    "username": "YourUsername",
    "password": "YourPassword",
    "email": "YourEmail@SomeDomain.com"
}
crawler = TwitterCrawler(account)
```

#### `TwitterCrawler.get_followings(user: str, verbose: bool = True) -> pd.DataFrame or None`

This method is used to crawl a specific Twitter user's followings.

- `user`: A Twitter user name.
- `verbose`: If `True`, print the progress.

If that account neither exists or suspended or doesn't follow anyone, return `None`. Otherwise, return a `pd.DataFrame` contains following information:

- `link`: The link of the user.
- `name`: The name of the user.
- `id`: The id of the user.

Example `DataFrame` followings of [@IvePetThatDog](https://twitter.com/IvePetThatDog):
| link                                  | name              | id               |
| ------------------------------------- | ----------------- | ---------------- |
| <https://twitter.com/dogfather>       | matt              | @dogfather       |
| <https://twitter.com/TheGoldenRatio4> | The Golden Ratio  | @TheGoldenRatio4 |
| <https://twitter.com/bunsenbernerbmd> | Bunsen and BEAKER | @bunsenbernerbmd |
| <https://twitter.com/PAVGOD>          | ᴘᴀᴠʟᴏᴠ ᴛʜᴇ ᴄᴏʀɢɪ  | @PAVGOD          |
| <https://twitter.com/15outof10>       | 15/10 Foundation  | @15outof10       |

#### `TwitterCrawler.get_followers(user: str, verbose: bool = True) -> pd.DataFrame or None`

This method is used to crawl a specific Twitter user's followers.

- `user`: A Twitter user name.
- `verbose`: If `True`, print the progress.

If that account neither exists or suspended or doesn't have any follower, return `None`. Otherwise, return a `pd.DataFrame` contains follower information:

- `link`: The link of the user.
- `name`: The name of the user.
- `id`: The id of the user.

#### `TwitterCrawler.is_exist(user: str = None, page_loaded: bool = False ) -> bool`

To check if a specific Twitter user exists.

- `user`: A Twitter user name.
- `page_loaded`: When the page is already loaded, assign it to True, t will directly check that account is exist or not. Otherwise, it will load the page first.

Return `True` if the user exists, otherwise return `False`.

#### `TwitterCrawler.have_followers(user: str = None, page_loaded: bool = False) -> bool`

To check if a specific Twitter user has followers.

- `user`: A Twitter user name.
- `page_loaded`: When the page is already loaded, assign it to True, t will directly check that account is exist or not. Otherwise, it will load the page first.

Return `True` if the user has followers, otherwise return `False`.

#### `TwitterCrawler.have_followings(user: str = None, page_loaded: bool = False) -> bool`

To check if a specific Twitter user has followings.

- `user`: A Twitter user name.
- `page_loaded`: When the page is already loaded, assign it to True, t will directly check that account is exist or not. Otherwise, it will load the page first.

Return `True` if the user has followings, otherwise return `False`.
