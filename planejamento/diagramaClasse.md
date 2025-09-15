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

    class Endereco {
	    String bairro
	    String cidade
	    String estado
        String numero
        String logradouro
        String pais
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
    Endereco -- Propriedade
```