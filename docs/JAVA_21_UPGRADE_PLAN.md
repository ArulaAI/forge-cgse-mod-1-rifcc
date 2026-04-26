# Java 21 Upgrade Plan

Goal: upgrade the `cgse-lab1-java` module from Java 17 to Java 21 (LTS).

Prerequisites
- Install JDK 21 locally or in CI (Adoptium/Eclipse Temurin, Corretto, etc.).
- Ensure Maven runs with the expected JDK: `mvn -version`.

High-level steps
1. Confirm current Java usage and build: `mvn -v` and `mvn -DskipTests=false -U clean verify`.
2. Update `pom.xml` to target Java 21 (use `<release>` approach).
3. Update Maven plugin/tool versions if needed (maven-compiler-plugin, enforcer).
4. Update CI workflows and Dockerfiles to use Java 21 images.
5. Run full test suite and fix incompatibilities.
6. Document and commit changes; push and monitor CI.

Recommended `pom.xml` edits
- Add a property for the Java version and set maven-compiler-plugin to use `<release>`.

Example (insert or adapt into the project `pom.xml`):

```xml
<properties>
  <java.version>21</java.version>
  <maven.compiler.plugin.version>3.11.0</maven.compiler.plugin.version>
</properties>

<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>${maven.compiler.plugin.version}</version>
      <configuration>
        <release>${java.version}</release>
      </configuration>
    </plugin>
    <!-- Ensure enforcer allows the new JDK if enforcer is used -->
  </plugins>
</build>
```

Notes
- Using `<release>` is preferred over separate `<source>`/`<target>` for newer JDKs.
- If your project uses `maven-toolchains-plugin`, update `toolchains.xml` or CI toolchain to point to JDK 21.

CI updates (GitHub Actions example)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - run: mvn -B -U clean verify
```

Dockerfile snippet

Replace base image with a JDK 21 image (example: Eclipse Temurin):

```
FROM eclipse-temurin:21-jdk
WORKDIR /app
COPY target/*.jar app.jar
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

Testing and compatibility checks
- Run `mvn -U clean test` and fix compile/test failures.
- Use `jdeps` to inspect dependencies and detect removed APIs or strong encapsulation issues.
- If you use reflection or internal APIs, address modules / `--add-opens` needs.

Rollback strategy
- Commit changes on a feature branch. If issues appear, revert the branch or open a quick rollback PR.

Post-upgrade
- Update developer docs to require JDK 21 locally.
- Verify any downstream deployments (Docker base images, cloud build images) use Java 21.

Estimated effort
- Small project: ~1–3 hours for changes + CI run and fixes.
- Larger apps or those using internal APIs: may require additional fixes.

Next action suggestions
- I can automatically apply the `pom.xml` changes (add `java.version` property and maven-compiler-plugin config) and update CI/Dockerfile snippets — tell me to proceed.
