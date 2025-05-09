Некоторые фичи нашего банковского мобильного приложения предполагают отображение пользователю череды экранов. В качестве примера можно привести, например, оплату счета или оформление новой банковской карты. Почему не всегда можно ограничиться одним экраном? Слишком большая когнитивная нагрузка на пользователя, необходимо заполнить все поля и сразу. В связи с этим также актуальной становится проблема сохранения прогресса.

Что если давать пользователю есть слона по частям? Разделим интересующий нас процесс оформления карты на шаги и будем сохранять состояние после каждого шага в БД:

```kotlin
sealed class Step {
    abstract val fieldName: String
    abstract val prompt: String
    abstract fun validate(input: String): Boolean

    data class NameStep(val next: Continuation) : Step() {
        override val fieldName = "fullName"
        override val prompt = "Введите ваше полное имя"
        override fun validate(input: String) = ...
    }

    data class BirthdateStep(val next: Continuation) : Step() {
        override val fieldName = "birthdate"
        override val prompt = "Введите вашу дату рождения"
        override fun validate(input: String) = ...
    }

    data class PassportStep(val next: Continuation) : Step() {
        override val fieldName = "passport"
        override val prompt = "Введите серию и номер паспорта"
        override fun validate(input: String) = ...
    }

    data class FinalStep(val resultHandler: (ClientState) -> String) : Step() {
        override val fieldName = "confirm"
        override val prompt = "Подтвердите отправку"
        override fun validate(input: String) = ...
    }
}

sealed class Continuation {
    data class Next(val step: Step) : Continuation()
    object Final : Continuation()
}

data class State(val inputs: MutableMap<String, String> = mutableMapOf()) {
    fun record(field: String, value: String) {
        inputs[field] =
            value // производим запись в БД, запись должна дополняться уникальными идентификаторами пользователя и процесса
    }
}

fun Step.handle(input: String, state: State): Continuation {
    if (!this.validate(input)) {
        throw IllegalArgumentException("Неверный ввод для поля $fieldName")
    }

    state.record(fieldName, input)

    return when (this) {
        is Step.NameStep -> this.next
        is Step.BirthdateStep -> this.next
        is Step.DocumentStep -> this.next
        is Step.FinalStep -> {
            val result = this.resultHandler(state)
            println("Заявка завершена: $result")
            Continuation.Final
        }
    }
}

val flow: Step = Step.NameStep(
    Continuation.Next(
        Step.BirthdateStep(
            Continuation.Next(
                Step.PassportStep(
                    Continuation.Next(
                        Step.FinalStep { state ->
                            "Новая карта оформлена для ${state.inputs["fullName"]}, " +
                                    "дата рождения: ${state.inputs["birthdate"]}, " +
                                    "документ: ${state.inputs["passport"]}"
                        }
                    )
                )
            )
        )
    )
)
```

Таким образом мы можем формировать и редактировать цепочки динамически. В целом это может послужить отправной точкой для формирования DSL для описания таких сценариев.
