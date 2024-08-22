Trabalho de Redes de Computadores para simular um chat de conversas:

    EXECUTAR
    - Se necessário instale a versão python 3.10
    - Depois inicie o servidor com o comando python s.py
    - E para iniciar a interface comando python main.py

0790528059800

    CLIENT PROTOCOL SEND:
    COD |                    ACTION                      |   STRUCTURE
--------|------------------------------------------------|--------------------------------------------------------|
[✔]  01 | Try Register in Server                         |  [COD(2)]
[✔]  03 | Try Notify the User is Online                  |  [COD(2)][ID(13)]
[✔]  05 | Try Send a Message to a other User             |  [COD(2)][SRC(13)][DST(13)][TIMESTAMP(10)][MSG(218)]
[✔]  08 | Try Notify the User is Seen Message Received   |  [COD(2)][SRC(13)][TIMESTAMP(10)]
[ ]  10 | Try Create a Group                             |
    
    CLIENT PROTOCOL RECEIVE:
    COD |                    ACTION                      |   STRUCTURE
--------|------------------------------------------------|--------------------------------------------------------|
[✔]  02 | Confirm Register and Receive ID                |  [COD(2)][ID(13)]
[✔]  06 | Receive Message                                |  [COD(2)][SRC(13)][DST(13)][TIMESTAMP(10)][MSG(218)]
[✔]  07 | Confirm Send Message                           |  [COD(2)][DST(13)][TIMESTAMP(10)]
[✔]  09 | Receive Seen                                   |  [COD(2)][SRC(13)][TIMESTAMP(10)]
[ ]  11 | Add in a Group                                 |

    SERVER PROTOCOL SEND:
    COD |                    ACTION                      |   STRUCTURE
--------|------------------------------------------------|--------------------------------------------------------|
[✔]  02 | Confirm Register and Receive ID                |  [COD(2)][ID(13)]
[✔]  06 | Receive Message                                |  [COD(2)][SRC(13)][DST(13)][TIMESTAMP(10)][MSG(218)]
[✔]  07 | Confirm Send Message                           |  [COD(2)][DST(13)][TIMESTAMP(10)]
[✔]  09 | Receive Seen                                   |  [COD(2)][SRC(13)][TIMESTAMP(10)]
[ ]  11 | Add in a Group                                 |
    
    SERVER PROTOCOL RECEIVE:
    COD |                    ACTION                      |   STRUCTURE
--------|------------------------------------------------|--------------------------------------------------------|
[✔]  01 | Register in Server                         |  [COD(2)]
[✔]  03 | Try Notify the User is Online                  |  [COD(2)][ID(13)]
[✔]  05 | Try Send a Message to a other User             |  [COD(2)][SRC(13)][DST(13)][TIMESTAMP(10)][MSG(218)]
[✔]  08 | Try Notify the User is Seen Message Received   |  [COD(2)][SRC(13)][TIMESTAMP(10)]
[ ]  10 | Try Create a Group                             |
