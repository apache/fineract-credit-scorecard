# Credit Scorecard Plugin for Apache Fineract

This is a [_Plugin_ for Apache Fineract](https://github.com/apache/fineract/blob/develop/fineract-doc/src/docs/en/deployment.adoc). 
(This work is inspired by the design approach of the [fineract-pentaho plugin](https://github.com/openMF/fineract-pentaho).)

see [TODO](TODO.md) for possible future follow-up enhancement work. The TODO list was inherited from [fineract-pentaho plugin]((https://github.com/openMF/fineract-pentaho))


## Build & Use

This project is currently only tested against the very latest and greatest
bleeding edge Fineract `develop` branch.  Building and using it against
older versions may be possible, but is not tested or documented here.

    git clone https://github.com/apache/fineract.git
    cd fineract && ./gradlew bootJar && cd ..

    git clone https://github.com/apache/fineract-credit-scorecard.git
    cd fineract-credit-scorecard && ./gradlew -x test distZip && cd ..

    ./fineract-credit-scorecard/scorecard-plugin/run

The [`run`](run) script basically just creates the following directory structure:

    fineract-provider.jar
    lib/scorecard-plugin.jar
    lib/lib*.jar

and then launches Apache Fineract with the Pentaho Plugin and all its JARs like this:

    java -Dloader.path=lib/ -jar fineract-provider.jar

## Contribute

If this Fineract plugin project is useful to you, please contribute back to it (and
Fineract) by raising Pull Requests yourself with any enhancements you make, and by helping
to maintain this project by helping other users on Issues and reviewing PR from others
(you will be promoted to committer on this project when you contribute).  We recommend
that you _Watch_ and _Star_ this project on GitHub to make it easy to get notified.
