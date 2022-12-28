# X-Touch Mini FS2020 Template Maker

Utility to turn your [X-Touch Mini FS2020](https://github.com/maartentamboer/X-Touch-Mini-FS2020) configs into SVGs.

The SVGs have transparent regions and can be used with commercial paper desktop CNCs such as the Cricut (Print & Cut) to quickly generate templates.

This allows you to rapidly experiment with and change your bindings.

## Pre-requsites

1. [X-Touch Mini FS2020](https://github.com/maartentamboer/X-Touch-Mini-FS2020)
2. Python3.9+

Enable [long path support](https://www.thewindowsclub.com/how-to-enable-or-disable-win32-long-paths-in-windows-11-10) if you haven't already done that as part of the python install.

Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run:

```
python -m template_maker.main --config c:\bin\X-Touch-Mini-FS2020\Configurations\config_longitude.bak.json --preview
```

## Current limitations

- only processes values for layer a (since this is all I use)
- file watch not implemented

PRs are welcomed.

## Inspiration

[Reddit: r/Behringer - Behringer X-Touch mini - Free Layout](https://www.reddit.com/r/Behringer/comments/k0xeeg/behringer_xtouch_mini_free_layout/) and the corresponding link to [Draw.io](https://viewer.diagrams.net/index.html?highlight=0000ff&edit=_blank&nav=1&title=Behringer%20X-Touch%20mini.drawio#R3Zpbb9owGIZ%2FDZe1fD7clnZM09ZNYlO33mXEkEgBszQdtL9%2BDjjNETXVqOokXJC8tmP7yYf9vSgTMl3vZ2mwjb6YUCcTDMP9hFxNMEZKQPuVK49OQZgdlVUah04rhXn8pJ3oGq4e4lDf1ypmxiRZvK2LC7PZ6EVW04I0Nbt6taVJ6r1ug5VuCfNFkLTV2zjMomIaXJUFH3W8ilzXEotjwTooKruZ3EdBaHYViVxPyDQ1JjuerfdTneT0Ci7Hdh9OlD4PLNWbrE%2BD1cWaLJfbH78%2FmdtfPxdJ%2FP3z9YW7y98geXATdoPNHgsCqXnYhDq%2FCZqQy10UZ3q%2BDRZ56c4%2BdKtF2Tpxxcs4SaYmMemhLbk8fKzeHmzRs04zva9IbvAzbdY6Sx9tlaKUO5AulIh017vKc8FCAYapej6OVaLKE6IQASZIWYW7aHGRsnruuYRpTxzPbrZ35ubP1d18821GvqqnCM9ubvdnZ3sCWAfW0wwFA4LVMapSqpGkEkDcwY8ICKCQ%2Fw%2BtMyDpy9DsXeyvX78MLLjfHpeEZbzPITejc3o4ct1sMrf0EFVcuw5PMX5N6BKKQZ06pe3gVRLQYnWsAs918ka4yRhx25UQQATLw1P2cozwKaeexnoxjHHxZpL7yhuPkbeA0lfeo9w7JYG%2B8uZj5K2Yr7kKHeV%2BiaDwdcNkPTbM17nDkiVSb%2BsWMWWA16gyiYCgLbBUAFysnDWbwyzYNyN7dt%2F9nmQ5l%2F6Q7ZF0%2BEqWWI5Q%2BRu0Pcyir2ipgl6j7ZG6%2BYqWI%2BwvVzZcroJQf7n2SH195SqZx3mBGC5XVfwn7CPXHtbBV64IQbt3VQ5%2Fl1s%2BYMPQkXz5lNfyATsGm3z5y3XAfqGZeXnFdcBmoZl5ecV1wE6hmXl5xXXATqGZeXnFdcBO4YXMyyfMYsDbGCJEANQwZar9F%2Fj7gB3wPtYF1qugPftedoJlk%2Fk52GJGAa37BcogkLzFFiEgEWqzxVwAgc7w9lknXDlgw4AIlUCJ%2BoqArc8lLbiYAF7MrAa3or%2BCrb0s38g8lFVebCXX%2FwA%3D) is where I got the first version of the measurements from, unfortunately I think it is in inches :-(.

Verious MDN documentation:

- [Getting Started with SVG](https://developer.mozilla.org/en-US/docs/Web/SVG)
- [SVG element reference](https://developer.mozilla.org/en-US/docs/Web/SVG/Element)
- [Positions](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Positions)
- [fill-opacity](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-opacity)
- [<rect>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect)

Various Stack Overflow documentation:

- [SVG rounded corner](https://stackoverflow.com/questions/10177985/svg-rounded-corner)
- [Subtract one circle from another in SVG](https://stackoverflow.com/questions/22579508/subtract-one-circle-from-another-in-svg)
- [Convert SVG to PNG in Python](https://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python)

And finally December.com: [Scalable Vector Graphics Color Names](https://www.december.com/html/spec/colorsvg.html).
