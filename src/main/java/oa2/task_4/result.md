Представим класс ReportGenerator, который должен генерировать отчёты разных форматов (например, Excel, Word или PDF). Нам бы хотелось при добавлении нового формата не изменять "точку входа", расширяя его возможности новыми "модулями".

Мы можем определить интерфейс ReportStrategy с методом generate(Data data), который будет реализован классами с различными стратегиями генерации отчетов:

```java
interface ReportStrategy {
    void generate(Data data);
}
```

```java
class PDFReportStrategy implements ReportStrategy {
    @Override
    public void generate(Data data) {
        // генерация PDF-отчёта
    }
}
```

```java
class ExcelReportStrategy implements ReportStrategy {
    @Override
    public void generate(Data data) {
        // генерация Excel-отчёта
    }
}
```

Класс ReportGenerator должен работать в соответствии с переданной стратегией:

```java

class ReportGenerator {
    private ReportStrategy reportStrategy;

    public ReportGenerator(ReportStrategy reportStrategy) {
        this.reportStrategy = reportStrategy;
    }

    void generateReport(Data data) {
        reportStrategy.generate(data);
    }
}
```

Таким образом, ReportGenerator теперь открыт для расширения (можно легко добавить новые способы генерации отчетов), но закрыт для изменений (его код не нужно изменять при добавлении новых форматов отчетов). Это обеспечивает гибкость и уменьшает риск внесения ошибок при модификации существующего кода.