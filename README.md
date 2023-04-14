# SPTeam - tablut

UCT-based agent that plays Tablut with
[Ashton rules](https://github.com/Scheggetta/SPTeam-tablut/blob/master/tablut_ashton_rules.pdf).

The slides of our project are available
[here](https://github.com/Scheggetta/SPTeam-tablut/blob/master/project_slides.pdf).

## Competition results

Our team placed in 3rd position! Competition results will be published
[here](http://ai.unibo.it/games/boardgamecompetition/tablut).

## Installation

The following guide assumes you are using a Linux operating system to run our program.

### Dependencies

- Python 3.9 or above / Pypy 3.9 or above (at least one of them)
- Java 8 (installation [guide](https://opensource.com/article/19/11/install-java-linux))
- git (installation [guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))

### Get repository
Run the following command on a clean terminal:
```
git clone https://github.com/Scheggetta/SPTeam-tablut
```

### PyPy

As a performance booster we warmly advice to use PyPy just-in-time interpreter.

Run the following command on a clean terminal:
<pre>
# Replace <i>/path/to/SPTeam-tablut</i> with <i>SPTeam-tablut</i> folder location
cd /path/to/SPTeam-tablut

curl https://downloads.python.org/pypy/pypy3.9-v7.3.9-linux64.tar.bz2 -o pypy.tar.bz2
mkdir pypy && tar -xf pypy.tar.bz2 -C pypy --strip-components=1
</pre>

## How to run

There are three possible configurations:
- *UCT* agent vs *random* agent
- *UCT* agent vs *UCT* agent
- *random* agent vs *random* agent (that's boring ｡^‿^｡)

In all three configurations it's necessary to open three terminals:
1. for the server
2. for the white agent
3. for the black agent

The way you launch both server and agents is equal for all configurations. What changes
are the agents' parameters.

### Agents' parameters

- `player`: can be `WHITE` or `BLACK`.
- `timeout`: positive integer that represents the time in seconds available to the agent
before sending a move to the server. Both agents don't necessarily have to set the same
`timeout` value.
- `ip_address`: server ip address. If the agent runs on the same machine as the server,
set `ip_address` to `localhost`.

### Terminal instructions
First, run the server:
<pre>
cd /path/to/SPTeam-tablut
java -jar Server.jar
</pre>

Second, run the first agent and then the second one.

#### Random agent
To run the random agent:
<pre>
cd /path/to/SPTeam-tablut

# Replace <i>player</i>, <i>timeout</i> and <i>ip_address</i> according to Agents' parameter section
java -jar RandomPlayer.jar &lt;player> &lt;timeout> &lt;ip_address>
</pre>

#### UCT agent
To run the UCT agent:
<pre>
cd /path/to/SPTeam-tablut
./pypy/bin/pypy3 main.py &lt;player> &lt;timeout> &lt;ip_address>
</pre>


## SPTeam
- [Angelo Quarta](https://github.com/NglQ)
- [Edoardo Fusa](https://github.com/Scheggetta)

## Credits

- Files `Server.jar` and `RandomPlayer.jar` taken from
[UniBo Tablut Competition repository](https://github.com/AGalassi/TablutCompetition).
- File `tablut_ashton_rules.pdf` made by Prof. Michela Milano.
