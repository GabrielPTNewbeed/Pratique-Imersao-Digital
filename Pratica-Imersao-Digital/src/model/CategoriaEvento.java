// src/main/java/br/com/yourevent/model/CategoriaEvento.java
package br.com.yourevent.model;

public enum CategoriaEvento {
    FESTA("Festa"),
    ESPORTIVO("Evento Esportivo"),
    SHOW("Show"),
    CULTURAL("Evento Cultural"),
    GASTRONOMICO("Evento Gastronômico"),
    EDUCACIONAL("Evento Educacional");

    private final String descricao;

    CategoriaEvento(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}