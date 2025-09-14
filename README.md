![CI (dev/staging/main)](https://img.shields.io/github/actions/workflow/status/AdaaJr/ai-service-boilerplate/ci.yml?branch=dev&label=CI)


# 🚀 Mon Infra AWS Sécurisée + CI/CD (2025)

Salut ! Je suis Wali et j’ai conçu cette infrastructure pour servir de **base pro prête à l’emploi** – autant pour les petits projets sérieux que pour des contextes **entreprise**.
Mon objectif : **mettre en prod rapidement, proprement et en sécurité** grâce à **Terraform** et **GitHub Actions (OIDC)**, sans secrets statiques.

![Architecture](diagrams/architecture.png)

## 🔎 C’est quoi exactement ?
Une infra AWS moderne et sécurisée, pensée “production” :
- **VPC** (eu-west-3) avec subnets publics/privés, NAT, endpoints VPC
- **ECS Fargate** derrière **ALB** (HTTPS via **ACM**) pour déployer une API/container
- **RDS PostgreSQL** privé, chiffré **KMS**, backups automatiques
- **S3 privé + CloudFront + WAF** pour le contenu statique
- **IAM** avec **GitHub OIDC** (assume-role, zéro secret)
- **Observabilité & sécurité** : CloudTrail, AWS Config, GuardDuty, SecurityHub, Access Analyzer
- **Supply chain** : scans (tfsec, gitleaks, Trivy), **SBOM** (Syft), signature d’images (cosign), provenance (SLSA-lite)

## 🎯 À quoi ça sert ?
- Déployer une **app containerisée** en HTTPS rapidement
- Disposer d’une **pipeline CI/CD** sécurisée réutilisable
- Servir de **référence pédagogique** (DevOps / Cloud / Sécurité)

---

## ⚙️ Prérequis
- Un compte **AWS**
- **Terraform ≥ 1.6** et **Docker** installés
- Un **repo GitHub** avec GitHub Actions activé

## 🔑 Secrets GitHub à créer
Dans votre repo → *Settings → Secrets and variables → Actions* :
- `AWS_ROLE_ECR_PUSH_ARN` → ARN du rôle `ecr-push` (créé par Terraform)
- `AWS_ROLE_TF_DEPLOYER_DEV_ARN` → ARN du rôle `tf-deployer-dev`
- `ECR_REPOSITORY_URI` → URL du repository ECR (ex. `123456789012.dkr.ecr.eu-west-3.amazonaws.com/aws-secure-infra`)

(Pour générer ces rôles/ressources : déployez l’environnement **dev** ci-dessous puis récupérez les **outputs Terraform**.)

---

## 🚀 Installation et premier déploiement

### 1) Cloner et initialiser
```bash
git clone https://github.com/AdaaJr/Infra-Aws-S-curis-e-Ci-cd.git
cd Infra-Aws-S-curis-e-Ci-cd
```

### 2) Déployer l’environnement **dev**
Éditez `infra/envs/dev/terraform.tfvars.example` avec vos valeurs (compte AWS, repo GitHub), puis :
```bash
cd infra/envs/dev
terraform init
terraform apply -auto-approve
```

### 3) Configurer les secrets GitHub
Récupérez dans les **outputs Terraform** : l’ARN du rôle `ecr-push`, l’ARN du rôle `tf-deployer-dev`, et l’URL du repo ECR.  
Ajoutez-les dans les **secrets GitHub** listés plus haut.

### 4) Déclencher la CI/CD
Revenez à la racine, créez la branche `dev` et poussez un changement :
```bash
git checkout -b dev
echo "ping" > ping.txt
git add ping.txt
git commit -m "Test CI/CD"
git push -u origin dev
```
- **CI** construit l’app, génère la **SBOM**, scanne IaC/secrets/containers, pousse l’image dans **ECR** et fait un `terraform plan`.
- **CD (dev)** applique Terraform et **(dans la version complète)** met à jour le service ECS.

---

## 📦 Structure du dépôt (extrait)
```
.github/workflows/  # CI/CD (OIDC)
app/                # API Go + Dockerfile
infra/
  modules/          # Terraform modules (vpc, oidc, ecr, ...)
  envs/dev/         # Environnement dev
diagrams/           # Diagrammes d’architecture
```

## 🧰 Bonnes pratiques intégrées
- **Least privilege** IAM par environnement
- **Chiffrement KMS** (S3, logs, RDS, ECR, secrets)
- **WAF** et **ALB** en HTTPS
- **Logs centralisés** (CloudWatch, S3)
- **Scans** automatiques + **SBOM**
- **Politique “no public S3 / no 0.0.0.0/0”** (dans la version complète via OPA/Conftest)

---

## 🙋‍♂️ Auteur
Je m’appelle **Wali Diabi**. J’ai ouvert ce repo pour aider celles et ceux qui veulent **apprendre** et **déployer** une infra AWS **sûre** sans repartir de zéro.
Si ça t’aide, une ⭐️ sur le repo me fera plaisir. Et si tu veux contribuer, ouvre une PR/issue !

```
Made with ❤️ & security-first mindset — 2025
```


---

## ❓ FAQ

### 💰 Combien ça coûte ?
- **Dev** : quelques euros / mois (VPC, ALB, ECS, RDS t3.micro, logs, S3)
- **Staging/Prod** : dépend des tailles (ECS tasks, RDS multi-AZ). Pensez au **Free Tier AWS** si applicable.

### ⚡ Puis-je personnaliser ?
Oui ! Modifiez les variables Terraform (`infra/envs/*/terraform.tfvars`) :
- `aws_region`
- `project_name`
- tailles d’instances RDS/ECS
- nombre d’AZ / subnets

### 🔐 Et la sécurité ?
Tout est sécurisé par défaut :
- Pas de S3 public
- Pas de `0.0.0.0/0` sur les SG
- TLS 1.2+ seulement
- KMS partout
- CI/CD sans secrets statiques

### 🧑‍💻 Puis-je réutiliser cette infra pour mes propres projets ?
Oui, c’est le but ! Forkez le repo, changez les valeurs, et déployez vos apps.

---
