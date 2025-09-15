# Diagrama de classes

A fim de mapear as entidades existentes, foi realizado um diagrama de classes simples.

O intuito não é documentar de forma extremamente precisa, mas apenas aglomerar as propriedades identificadas no desafio em um meio de fácil consulta. 


```mermaid
classDiagram

direction TB

    class Propriedade {
	    String nome
	    int numeroQuartos
	    int capacidadeMaxPessoas
	    Decimal precoNoite
    }

    class Localizacao {
	    String bairro
	    String cidade
	    String siglaEstado
    }

    class Cliente {
	    String nome
        String email
    }

    class Reserva {
	    Date inicio
	    Date fim
	    int numeroOcupantes
        boolean ativa
        Decimal valorTotal
    }

    Reserva --* Propriedade
    Cliente -- Reserva : realiza
    Localizacao -- Propriedade
```