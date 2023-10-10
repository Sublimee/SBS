@Service
public class FirstService {

    private final SecondService secondService;

    @Autowired
    public FirstService(SecondService secondService) {
        this.secondService = secondService;
    }

    public ResponseExample.ResponseExampleBuilder buildFirstPart(String firstPart) {
        return BuilderObject.builder()
                .setFirstPart(firstPart)
    }
}

@Service
public class SecondService {

    private final ThirdService thirdService;

    @Autowired
    public SecondService(ThirdService thirdService) {
        this.thirdService = thirdService;
    }

    public ResponseExample.ResponseExampleBuilder buildSecondPart(ResponseExample.ResponseExampleBuilder responseBuilder,
                                                                  String secondPart) {
        return thirdService(responseBuilder.setSecondPart(secondPart));
    }
}

@Service
public class ThirdService {

    ...

    public ResponseExample buildThirdPart(ResponseExample.ResponseExampleBuilder responseBuilder) {
        return response.setThirdPart("Third part").build();
    }
}

@Builder
public class ResponseExample {
    private String firstPart;
    private String secondPart;
    private String thirdPart;
}