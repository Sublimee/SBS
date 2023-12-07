package oa2.task_1;


// Класс Расы для демонстрации композиции
class Race {

    private final String name;

    private final String home;

    private final double powerMultiplier;
    private final double agilityMultiplier;
    private final double intelligenceMultiplier;

    public Race(String name, String home, double powerMultiplier, double agilityMultiplier, double intelligenceMultiplier) {
        this.name = name;
        this.home = home;
        this.powerMultiplier = powerMultiplier;
        this.agilityMultiplier = agilityMultiplier;
        this.intelligenceMultiplier = intelligenceMultiplier;
    }

    public String getName() {
        return name;
    }

    public double getPowerMultiplier() {
        return powerMultiplier;
    }

    public double getAgilityMultiplier() {
        return agilityMultiplier;
    }

    public double getIntelligenceMultiplier() {
        return intelligenceMultiplier;
    }

    public String getHome() {
        return home;
    }
}

// Базовый класс Персонаж, каждый Персонаж имеет Расу
abstract class Character {

    private String name;

    private Race race;

    private int basePower;
    private int baseAgility;
    private int baseIntelligence;

    public Character(Race race, int basePower, int baseAgility, int baseIntelligence, String name) {
        this.race = race;
        this.basePower = basePower;
        this.baseAgility = baseAgility;
        this.baseIntelligence = baseIntelligence;
        this.name = name;
    }

    public Race getRace() {
        return race;
    }

    public void setRace(Race race) {
        this.race = race;
    }

    public int getPower() {
        return (int) (basePower * race.getPowerMultiplier());
    }

    public int getAgility() {
        return (int) (baseAgility * race.getAgilityMultiplier());
    }

    public int getIntelligence() {
        return (int) (baseIntelligence * race.getIntelligenceMultiplier());
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setBasePower(int basePower) {
        this.basePower = basePower;
    }

    public void setBaseAgility(int baseAgility) {
        this.baseAgility = baseAgility;
    }

    public void setBaseIntelligence(int baseIntelligence) {
        this.baseIntelligence = baseIntelligence;
    }

    public String greeting() {
        return "Hello! My name is " + name + "! I,m from " + race.getName() + ".";
    }

    void backHome() {
        System.out.println("Back to " + getRace().getHome());
    }
}

// Подкласс Бот, наследующийся от Персонажа
class Bot extends Character {

    public Bot(Race race, int basePower, int baseAgility, int baseIntelligence, String name) {
        super(race, basePower, baseAgility, baseIntelligence, name);
    }

    @Override
    public String greeting() {
        return super.greeting() + " I'm bot.";
    }
}

// Подкласс Игрок, наследующийся от Персонажа
class Player extends Character {

    private Integer guildId;

    public Player(Race race, int basePower, int baseAgility, int baseIntelligence, String name, int guildId) {
        super(race, basePower, baseAgility, baseIntelligence, name);
        this.guildId = guildId;
    }


    public Integer getGuildId() {
        return guildId;
    }

    public void setGuildId(Integer guildId) {
        this.guildId = guildId;
    }

    @Override
    public String greeting() {
        return super.greeting() + " I'm player.";
    }
}


public class Main {
    public static void main(String[] args) {
        Race human = new Race("Humans", "Stormwind City", 1, 1, 2);
        Character character1 = new Bot(human, 1, 1, 1, "WX1");

        Race troll = new Race("Trolls", "Orgrimmar", 1, 2, 1);
        Character character2 = new Player(troll, 1, 1, 1, "Alex", 1);

        // Полиморфизм: использование объектов Бот и Игрок как Персонажей
        System.out.println(character1.greeting()); // Вызывает метод greeting() класса Bot
        System.out.println(character2.greeting()); // Вызывает метод greeting() класса Player

        // Персонаж имеет Расу, которая параметризует поведение
        character1.backHome();
        character2.backHome();
        // Поведение также параметризуется и при вызове greeting()
    }
}