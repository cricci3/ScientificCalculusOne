package org.example;

public class SystemInfo {
    private String language;
    private String operatingSystem;

    public SystemInfo() {
        this.language = "Java";
        this.operatingSystem = System.getProperty("os.name");
    }

    public String getLanguage() { return language; }
    public void setLanguage(String language) { this.language = language; }
    public String getOperatingSystem() { return operatingSystem; }
    public void setOperatingSystem(String operatingSystem) { this.operatingSystem = operatingSystem; }
}