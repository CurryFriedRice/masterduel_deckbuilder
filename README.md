# Yu-gi-oh Deck Builder

This is a deck building application for the TCG/OCG Yu-gi-oh that leverages the unofficial Yu-gi-oh API to fetch card data; alongside Python, SQL, and Flask to create a reactive deckbuilding experience.

This application was inspired by the release of Yu-Gi-Oh Master Duel. It uses the Yu-Gi-Oh Api by Prodeck.

I understand that there is a lot that can still be done and bugs that can be fixed; the purpose of this project was to build out a Mininum Viable Product. In this case it is an online deckbuilding experience that you can just boot up, login, and start building right away.

This is not a commercial product and was built for educational purposes all card images belong to Konami Holdings.

# Features

<h2>User Registration</h2>
<table>
    <tr>
        <td width=50%>
            <p>Users must register to the site to use it.</p>
            <p>Each username and email must be unique so we can properly attach items to the user.</p>
            <p>It's a simple login form where the user has to also agree to the mock eula.</p>
        </td>
        <td width=50%>
            <img src=./readme_assets/login.png alt="Login Form"style="width:500px">
        </td>
    </tr>
</table>

<h2>Deck Viewing</h2>
<table>
    <tr>
        <td width=50%>
            <p>The list of decks are shown on the main dashboard.</p>
            <p>When a deck is created it has a name and as such a user can filter out a deck based on what it was named.</p>
            <p>By clicking on a username you are able to filter out decks made by that user.</p>
        </td>
        <td width=50%>
            <img src=./readme_assets/dashboard.gif alt="Dashboard Gif"style="width:500px">
        </td>
    </tr>
</table>

<h2>Deck Building</h2>

<h3>Searching Cards</h3>
<table>
    <tr>
        <td width=50%>
            <p>Through the use of the Yu-gi-oh API we are able to search through the thousands of cards by looking up their card names.</p>
            <p>The images that are loaded are saved from the API database to local storage to reduce the amount of calls to the API.</p>
        </td>
        <td width=50%>
            <img src=./readme_assets/card-search.gif alt="Deck Builder Gif"style="width:500px">
        </td>
    </tr>
</table>


<h3>Adding Cards</h3>
<table>
    <tr>
        <td width=50%>
            <p>There are two primary ways that the user can add cards to their deck.</p>
            <p>The first is by clicking and dragging it from the results to the deck area. The second is by using a keyboard command while hovering over the card by pressing 'a'.</p>
            <p>When the card is added it will be grouped up if there are multiple copies.</p>
        </td>
        <td width=50%>
            <img src=./readme_assets/card-add.gif alt="Deck Builder Gif"style="width:500px">
        </td>
    </tr>
</table>


<h3>Removing Cards</h3>
<table>
    <tr>
        <td width=50%>
            <p>A user can remove cards from their deck by dragging it from the deck into the search pile.</p>
            <p>Alternatively they can use the 's' key to subtract the card from their deck.</p>
            <p></p>
        </td>
        <td width=50%>
            <img src=./readme_assets/card-subtract.gif alt="Deck Builder Gif"style="width:500px">
        </td>
    </tr>
</table>

<h3>Card Details</h3>
<table>
    <tr>
        <td width=50%>
            <p>More often than not a card has a ton of text on it; and I'm not going to make you squint to read it.</p>
            <p>A user can hit 'd' to enable a detailed view. The view contains pertinent information about the card.</p>
            <p></p>
        </td>
        <td width=50%>
            <img src=./readme_assets/card-details.png alt="Deck Builder Gif"style="width:500px">
        </td>
    </tr>
</table>

<h3>Deck Validation</h3>
<table>
    <tr>
        <td width=50%>
            <p>There are limits to what the user can add to a deck. The two most important ones are size and copies of a card.</p>
            <p>Currently a deck is valid if it has at least 40 cards and a maximum of 3 copies of each card.</p>
        </td>
        <td width=50%>
        </td>
    </tr>
</table>

# Future plans.

There is still a lot to do to improve the application experience. For starters the styling of the page needs to be improved from basic developer stylings. After that there's better displays for the detailed views. 

Another place that could be improved is  deck validation. Currently it just does a baseline check of whether or not 3 or more copies are in the deck. There are Finer deck rules like Semi-Limited, Limited, and Forbidden cards.

There's also better searching that could be done, like searching for a card by name then by descriptions such that if you searched something broad like 'negate' you could find all cards that contain 'negate.'

Another feature would be deck price in both OCG/TCG and Master Duel. This way a player can calculate how much currency they are willing to put into a deck.

Overall, I am satisfied with how this project turned out within a week of development. At the start it was overwhelming with the sheer amount of data that I was recieving and what I could do with it. But by stepping back and breaking down into user stories and features I was able to build a bit at a time to create something I believed was out of reach.