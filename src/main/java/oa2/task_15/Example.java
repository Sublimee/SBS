package oa2.task_15;

class ChannelV1 {

    private final boolean isPartner;

    public ChannelV1(boolean isPartner) {
        this.isPartner = isPartner;
    }

    public boolean isPartner() {
        return isPartner;
    }
}

class ChannelV2 {

    private final Partnership partnership;

    public ChannelV2(Partnership partnership) {
        this.partnership = partnership;
    }

    public boolean isPartner() {
        return partnership.isPartner();
    }
}

abstract class Partnership {
    public abstract boolean isPartner();
}

class Beeline extends Partnership {

    public boolean isPartner() {
        return true;
    }
}

class Megafon extends Partnership {

    public boolean isPartner() {
        return true;
    }
}

class Internal extends Partnership {

    public boolean isPartner() {
        return false;
    }
}