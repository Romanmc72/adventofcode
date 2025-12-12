# Advent Of Code 2025

I want to sit down and write some Swift this year! Never done it.

Actually that is a lie. I have tried to write swift a few times but had only the goal of making a mobile app. Then I found out that I needed a macbook and the only one I had was for work and they owned anything I made on that machine so I stopped and learned react native instead. Now I come back as a more seasoned developer and am interested in Swift just for the sake of learning it.

## Recreating this

I downloaded swift based on the online guide here:

https://www.swift.org/install/linux/

Then I ran

```sh
swift package init --name aoc --type executable
```

and started to follow the guide and ask Gemini how to do stuff.

## Running this

run it with

```sh
swift run aoc \
  <day#> \
  -p <part# (or blank for both)> \
  --example (optional, default = false)
```

## Tests

Oh yeah, there are some unit tests that I made for when I got stuck and wanted to debug which cases were tripping me up. To run those just run:

```sh
swift test
```

or if you want to run just one test or test case you can use the `--filter` flag like so:

```sh
swift test --filter Day05Tests.testExample
```
